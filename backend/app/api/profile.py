import time
import json
from datetime import datetime, timezone
from flask import Blueprint, jsonify, current_app
from backend.app.services.github_graphql import fetch_github_profile_raw
from backend.app.services.github_rest import fetch_user_repos, fetch_repo_languages, fetch_recent_commits
from backend.app.services.aggregator import calculate_metrics
from backend.app.services.cache_service import get_cached_profile, save_profile_to_cache
from backend.app.models.repo_snapshot import RepoSnapshot
from backend.app.models.fetch_log import FetchLog
from backend.app.extensions import db, redis_client

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/api/profile/<username>', methods=['GET'])
def get_profile(username):
    """
    Retrieves the aggregated profile statistics for a GitHub username.
    Day 2 implementation: Cache-first approach. Serves from database cache if available and fresh.
    Otherwise fetches from GitHub GraphQL + REST APIs, aggregates metrics, caches, and returns.
    """
    start_time = time.time()
    username_lower = username.lower()
    
    # 0. Check Redis short-term cache first
    redis_key = f"profile:response:{username_lower}"
    if redis_client:
        try:
            cached_resp_str = redis_client.get(redis_key)
            if cached_resp_str:
                cached_resp = json.loads(cached_resp_str)
                cached_resp["cached"] = True
                cached_resp["source"] = "redis_cache"
                duration_ms = int((time.time() - start_time) * 1000)
                current_app.logger.info(f"Redis cache hit for @{username_lower} in {duration_ms}ms")
                return jsonify(cached_resp)
        except Exception as e:
            current_app.logger.warning(f"Error reading from Redis cache: {e}")

    # 1. Check cache first
    try:
        cached = get_cached_profile(username_lower)
        if cached:
            # Load associated repositories snapshots
            snapshots = RepoSnapshot.query.filter_by(profile_id=cached.id).all()
            
            duration_ms = int((time.time() - start_time) * 1000)
            current_app.logger.info(f"Cache hit for @{username_lower} in {duration_ms}ms")
            
            response_data = {
                "status": "success",
                "source": "database_cache",
                "cached": True,
                "data": {
                    "profile": cached.to_dict(),
                    "repos": [r.to_dict() for r in snapshots],
                    "metrics": cached.metrics_json
                }
            }
            if redis_client:
                try:
                    ttl_seconds = current_app.config.get('RESPONSE_CACHE_TTL_SECONDS', 300)
                    redis_client.setex(redis_key, ttl_seconds, json.dumps(response_data))
                except Exception as ex:
                    current_app.logger.warning(f"Failed to cache database response to Redis: {ex}")
            return jsonify(response_data)
    except Exception as e:
        current_app.logger.error(f"Error checking cache for {username_lower}: {e}")
        # Proceed to fetch if cache lookup fails
        
    current_app.logger.info(f"Cache miss for @{username_lower}. Fetching from GitHub API...")
    
    # 2. Cache miss: Fetch and calculate
    api_calls = 0
    try:
        # A. Fetch Profile and Contributions from GraphQL (1 call)
        graphql_data = fetch_github_profile_raw(username_lower)
        api_calls += 1
        
        if not graphql_data:
            # Log failure fetch
            duration_ms = int((time.time() - start_time) * 1000)
            log_fetch_event(username_lower, 'full', api_calls, False, "User not found", duration_ms)
            return jsonify({"error": f"GitHub user '@{username_lower}' not found"}), 404
            
        # B. Fetch all repositories from REST (at least 1 call)
        repos_raw = fetch_user_repos(username_lower)
        api_calls += max(1, len(repos_raw) // 100) if repos_raw else 1
        
        if repos_raw is None:
            # Fallback check
            duration_ms = int((time.time() - start_time) * 1000)
            log_fetch_event(username_lower, 'full', api_calls, False, "User repos check 404", duration_ms)
            return jsonify({"error": f"GitHub user '@{username_lower}' not found"}), 404
            
        # C. Fetch languages for top 30 repos (max 30 calls)
        # Sort by star count desc, then push time desc
        def repo_sort_key(r):
            return (r.get('stargazers_count', 0), r.get('pushed_at', ''))
            
        sorted_repos = sorted(repos_raw, key=repo_sort_key, reverse=True)
        max_lang_repos = current_app.config.get('MAX_REPOS_FOR_LANGUAGE_DETAIL', 30)
        top_repos_for_langs = sorted_repos[:max_lang_repos]
        
        languages_by_repo = {}
        for r in top_repos_for_langs:
            owner = r.get('owner', {}).get('login')
            name = r.get('name')
            if owner and name:
                languages_by_repo[r['full_name']] = fetch_repo_languages(owner, name)
                api_calls += 1
                
        # D. Fetch recent commits for top 5 owned repositories to analyze patterns
        owned_repos = [r for r in repos_raw if not r.get('fork', False)]
        owned_repos_sorted = sorted(owned_repos, key=lambda r: r.get('stargazers_count', 0), reverse=True)
        top_5_repos = owned_repos_sorted[:5]
        
        commit_timestamps = []
        for r in top_5_repos:
            owner = r.get('owner', {}).get('login')
            name = r.get('name')
            if owner and name:
                commits = fetch_recent_commits(owner, name, username_lower)
                api_calls += 1
                for c in commits:
                    date_str = c.get('commit', {}).get('author', {}).get('date')
                    if date_str:
                        commit_timestamps.append(date_str)
                        
        # 3. Aggregate metrics
        calendar_data = graphql_data.get("contributionsCollection", {}).get("contributionCalendar", {})
        metrics = calculate_metrics(repos_raw, languages_by_repo, calendar_data, commit_timestamps)
        
        # 4. Save to cache
        cached_profile = save_profile_to_cache(
            username_lower,
            graphql_data,
            repos_raw,
            metrics,
            languages_by_repo
        )
        
        # Query the newly saved snapshots
        snapshots = RepoSnapshot.query.filter_by(profile_id=cached_profile.id).all()
        
        duration_ms = int((time.time() - start_time) * 1000)
        log_fetch_event(username_lower, 'full', api_calls, True, None, duration_ms)
        current_app.logger.info(f"Successfully cached and returned @{username_lower} in {duration_ms}ms (API calls: {api_calls})")
        
        response_data = {
            "status": "success",
            "source": "github_api",
            "cached": False,
            "data": {
                "profile": cached_profile.to_dict(),
                "repos": [r.to_dict() for r in snapshots],
                "metrics": metrics
            }
        }
        if redis_client:
            try:
                ttl_seconds = current_app.config.get('RESPONSE_CACHE_TTL_SECONDS', 300)
                redis_client.setex(redis_key, ttl_seconds, json.dumps(response_data))
            except Exception as ex:
                current_app.logger.warning(f"Failed to cache GitHub API response to Redis: {ex}")
        return jsonify(response_data)
        
    except ValueError as e:
        duration_ms = int((time.time() - start_time) * 1000)
        log_fetch_event(username_lower, 'full', api_calls, False, str(e), duration_ms)
        return jsonify({
            "status": "error",
            "error": "Configuration Error",
            "message": str(e)
        }), 500
    except IOError as e:
        duration_ms = int((time.time() - start_time) * 1000)
        log_fetch_event(username_lower, 'full', api_calls, False, str(e), duration_ms)
        return jsonify({
            "status": "error",
            "error": "GitHub API Error",
            "message": str(e)
        }), 502
    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)
        log_fetch_event(username_lower, 'full', api_calls, False, str(e), duration_ms)
        return jsonify({
            "status": "error",
            "error": "Internal Server Error",
            "message": str(e)
        }), 500

def log_fetch_event(username, fetch_type, api_calls, success, error_message, duration_ms):
    """
    Helper to record api fetch metadata in the FetchLog table.
    """
    try:
        log = FetchLog(
            username=username,
            fetch_type=fetch_type,
            api_calls_used=api_calls,
            success=success,
            error_message=error_message,
            duration_ms=duration_ms
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to record FetchLog for {username}: {e}")

@profile_bp.route('/api/health', methods=['GET'])
def health_check():
    """
    Exposes application health, database status, Redis connectivity, and GitHub rate limits.
    """
    from backend.app.services.rate_limit_service import get_rate_limits
    
    # Check DB connection
    db_ok = True
    try:
        db.session.execute(db.text("SELECT 1"))
    except Exception:
        db_ok = False
        
    # Check Redis connectivity
    redis_ok = (redis_client is not None)
    
    # Get Cached or Live Rate Limits
    rate_limits = get_rate_limits()
    
    return jsonify({
        "status": "healthy" if db_ok else "unhealthy",
        "database_connected": db_ok,
        "redis_connected": redis_ok,
        "github_token_configured": bool(current_app.config.get('GITHUB_TOKEN')),
        "github_rate_limits": rate_limits
    })
