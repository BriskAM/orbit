from datetime import datetime, timezone, timedelta
from backend.app.models.profile import CachedProfile
from backend.app.models.repo_snapshot import RepoSnapshot
from backend.app.extensions import db
from flask import current_app

def parse_iso_datetime(dt_str):
    """
    Parses ISO 8601 datetime strings returned by GitHub (e.g. '2011-01-25T18:44:36Z').
    """
    if not dt_str:
        return None
    try:
        # Standardize 'Z' to UTC offset representation for Python's fromisoformat
        clean_str = dt_str.replace('Z', '+00:00')
        return datetime.fromisoformat(clean_str)
    except Exception:
        return None

def get_cached_profile(username):
    """
    Retrieves a cached profile from the database.
    Checks if the cache has expired (based on PROFILE_CACHE_TTL_HOURS).
    Increments fetch_count if cache is fresh.
    Returns:
        CachedProfile instance or None if missing/stale.
    """
    username_lower = username.lower()
    profile = CachedProfile.query.filter_by(username=username_lower).first()
    if not profile:
        return None
        
    # Check if cached data is stale
    ttl_hours = current_app.config.get('PROFILE_CACHE_TTL_HOURS', 6)
    expiration_time = profile.last_fetched_at + timedelta(hours=ttl_hours)
    
    # Check tz-awareness compatibility
    now = datetime.now(timezone.utc)
    if profile.last_fetched_at.tzinfo is None:
        # If SQLite datetime is naive, compare with naive UTC
        now = datetime.now()
        
    if now > expiration_time:
        return None
        
    # Increment fetch count (view stats)
    try:
        profile.fetch_count += 1
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.warning(f"Failed to increment fetch_count for {username}: {e}")
        
    return profile

def save_profile_to_cache(username, profile_raw, repos_raw, metrics, languages_by_repo):
    """
    Saves a profile and its repository snapshots in a transaction.
    Inserts or updates the CachedProfile and replaces associated RepoSnapshots.
    """
    username_lower = username.lower()
    
    try:
        # Get or create profile
        profile = CachedProfile.query.filter_by(username=username_lower).first()
        if not profile:
            profile = CachedProfile(username=username_lower)
            db.session.add(profile)
            
        # Update CachedProfile fields
        profile.display_name = profile_raw.get('name')
        profile.avatar_url = profile_raw.get('avatarUrl')
        profile.bio = profile_raw.get('bio')
        profile.company = profile_raw.get('company')
        profile.location = profile_raw.get('location')
        profile.blog_url = profile_raw.get('websiteUrl')
        profile.twitter_username = profile_raw.get('twitterUsername')
        profile.follower_count = profile_raw.get('followers', {}).get('totalCount', 0)
        profile.following_count = profile_raw.get('following', {}).get('totalCount', 0)
        profile.public_repo_count = profile_raw.get('repositories', {}).get('totalCount', 0)
        profile.account_created_at = parse_iso_datetime(profile_raw.get('createdAt'))
        
        # Populate aggregated metrics
        profile.total_stars_earned = metrics.get('total_stars_earned', 0)
        profile.total_forks_received = metrics.get('total_forks_received', 0)
        profile.longest_streak_days = metrics.get('longest_streak_days', 0)
        profile.current_streak_days = metrics.get('current_streak_days', 0)
        profile.top_language = metrics.get('top_language')
        profile.language_breakdown = metrics.get('language_breakdown', {})
        profile.metrics_json = metrics
        
        # Force refresh timestamp
        profile.last_fetched_at = datetime.utcnow()
        
        # Flush to get the profile.id (if newly created)
        db.session.flush()
        
        # Clear existing RepoSnapshot entries for this user
        RepoSnapshot.query.filter_by(profile_id=profile.id).delete()
        
        # Insert new RepoSnapshot entries
        for r in repos_raw:
            snapshot = RepoSnapshot(
                profile_id=profile.id,
                repo_name=r.get('name'),
                full_name=r.get('full_name'),
                description=r.get('description'),
                is_fork=r.get('fork', False),
                primary_language=r.get('language'),
                languages_json=languages_by_repo.get(r.get('full_name'), {}),
                stars=r.get('stargazers_count', 0),
                forks=r.get('forks_count', 0),
                watchers=r.get('watchers_count', 0),
                open_issues=r.get('open_issues_count', 0),
                size_kb=r.get('size', 0),
                created_at=parse_iso_datetime(r.get('created_at')),
                pushed_at=parse_iso_datetime(r.get('pushed_at')),
                topics=r.get('topics', [])
            )
            db.session.add(snapshot)
            
        db.session.commit()
        return profile
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error saving profile cache for {username}: {e}")
        raise IOError(f"Failed to write profile to database cache: {e}")
