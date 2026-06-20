from flask import Blueprint, Response, current_app, jsonify
from backend.app.models.profile import CachedProfile
from backend.app.models.repo_snapshot import RepoSnapshot
from backend.app.services.og_image_service import generate_og_image_svg
from backend.app.services.github_graphql import fetch_github_profile_raw
from backend.app.services.github_rest import fetch_user_repos, fetch_repo_languages
from backend.app.services.aggregator import calculate_metrics
from backend.app.services.cache_service import save_profile_to_cache

meta_bp = Blueprint('meta', __name__)

@meta_bp.route('/api/meta/og-image/<username>', methods=['GET'])
def get_og_image(username):
    """
    Returns a dynamically generated SVG OpenGraph share card for a user.
    Serves from DB if cached, otherwise performs a fast fetch and caches the result.
    """
    username_lower = username.lower()
    
    try:
        # Check database cache first
        cached = CachedProfile.query.filter_by(username=username_lower).first()
        
        if not cached:
            current_app.logger.info(f"Cache miss for og-image @{username_lower}. Fetching data...")
            # Lightweight fetch for quick response
            graphql_data = fetch_github_profile_raw(username_lower)
            if not graphql_data:
                return Response(
                    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 630'>"
                    "<rect width='100%' height='100%' fill='#131318'/>"
                    "<text x='50%' y='50%' fill='#ffb4ab' font-family='sans-serif' font-size='30' text-anchor='middle'>"
                    "GitHub User Not Found"
                    "</text></svg>",
                    mimetype="image/svg+xml",
                    status=404
                )
                
            repos_raw = fetch_user_repos(username_lower) or []
            
            # Fetch languages for top 5 repos to save time during preview generation
            top_repos = sorted(repos_raw, key=lambda r: r.get('stargazers_count', 0), reverse=True)[:5]
            languages_by_repo = {}
            for r in top_repos:
                owner = r.get('owner', {}).get('login')
                name = r.get('name')
                if owner and name:
                    languages_by_repo[r['full_name']] = fetch_repo_languages(owner, name)
                    
            metrics = calculate_metrics(repos_raw, languages_by_repo)
            
            cached = save_profile_to_cache(
                username_lower,
                graphql_data,
                repos_raw,
                metrics,
                languages_by_repo
            )
            
        # Compile SVG payload
        profile_data = {
            "profile": cached.to_dict(),
            "metrics": cached.metrics_json or {}
        }
        
        svg_content = generate_og_image_svg(profile_data)
        
        return Response(svg_content, mimetype="image/svg+xml")
        
    except Exception as e:
        current_app.logger.error(f"Error generating og-image for {username_lower}: {e}")
        return Response(
            f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 630'>"
            f"<rect width='100%' height='100%' fill='#131318'/>"
            f"<text x='50%' y='50%' fill='#ffb4ab' font-family='sans-serif' font-size='24' text-anchor='middle'>"
            f"Error Generating Share Card"
            f"</text></svg>",
            mimetype="image/svg+xml",
            status=500
        )

@meta_bp.route('/api/meta/stats', methods=['GET'])
def get_global_stats():
    """
    Returns aggregated stats across all analyzed profiles in the Orbit system.
    """
    try:
        profiles = CachedProfile.query.all()
        total_profiles = len(profiles)
        
        if total_profiles == 0:
            # Return elegant default base metrics if no database records exist yet
            return jsonify({
                "total_profiles": 0,
                "total_repos": 0,
                "total_stars": 0,
                "total_commits": 0,
                "avg_repos": 0.0,
                "top_languages": {},
                "avg_night_owl_ratio": 0.0,
                "avg_early_bird_ratio": 0.0,
                "avg_longest_streak": 0.0
            })
            
        total_stars = sum(p.total_stars_earned or 0 for p in profiles)
        total_commits = sum(p.total_commits_last_year or 0 for p in profiles)
        total_repos = RepoSnapshot.query.count()
        avg_repos = round(total_repos / total_profiles, 1)
        
        languages = {}
        night_owl_ratios = []
        early_bird_ratios = []
        longest_streaks = []
        
        for p in profiles:
            if p.top_language:
                lang = p.top_language.strip()
                if lang:
                    languages[lang] = languages.get(lang, 0) + 1
            
            longest_streaks.append(p.longest_streak_days or 0)
            
            m = p.metrics_json or {}
            if 'night_owl_ratio' in m:
                night_owl_ratios.append(m['night_owl_ratio'])
            if 'early_bird_ratio' in m:
                early_bird_ratios.append(m['early_bird_ratio'])
                
        avg_night_owl = round(sum(night_owl_ratios) / len(night_owl_ratios), 3) if night_owl_ratios else 0.0
        avg_early_bird = round(sum(early_bird_ratios) / len(early_bird_ratios), 3) if early_bird_ratios else 0.0
        avg_longest_streak = round(sum(longest_streaks) / len(longest_streaks), 1) if longest_streaks else 0.0
        
        # Sort languages by frequency descending
        sorted_langs = dict(sorted(languages.items(), key=lambda item: item[1], reverse=True))
        
        return jsonify({
            "total_profiles": total_profiles,
            "total_repos": total_repos,
            "total_stars": total_stars,
            "total_commits": total_commits,
            "avg_repos": avg_repos,
            "top_languages": sorted_langs,
            "avg_night_owl_ratio": avg_night_owl,
            "avg_early_bird_ratio": avg_early_bird,
            "avg_longest_streak": avg_longest_streak
        })
    except Exception as e:
        current_app.logger.error(f"Error fetching global stats: {e}")
        return jsonify({"error": str(e)}), 500

