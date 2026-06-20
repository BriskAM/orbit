import requests
from flask import current_app
from backend.app.extensions import redis_client

# In-memory rate limit store for fallback
_in_memory_ratelimit = {
    "limit": None,
    "remaining": None,
    "reset": None
}

def update_rate_limits(limit, remaining, reset_timestamp):
    """
    Caches the latest rate limit details in Redis, falling back to local memory.
    """
    global _in_memory_ratelimit
    limit_val = int(limit) if limit is not None else None
    rem_val = int(remaining) if remaining is not None else None
    reset_val = int(reset_timestamp) if reset_timestamp is not None else None
    
    if redis_client:
        try:
            if limit_val is not None:
                redis_client.set("github:ratelimit:limit", limit_val)
            if rem_val is not None:
                redis_client.set("github:ratelimit:remaining", rem_val)
            if reset_val is not None:
                redis_client.set("github:ratelimit:reset", reset_val)
            return
        except Exception as e:
            current_app.logger.warning(f"Failed to cache rate limits in Redis: {e}")
            
    # Fallback to local memory
    if limit_val is not None:
        _in_memory_ratelimit["limit"] = limit_val
    if rem_val is not None:
        _in_memory_ratelimit["remaining"] = rem_val
    if reset_val is not None:
        _in_memory_ratelimit["reset"] = reset_val

def get_rate_limits():
    """
    Retrieves the current rate limits.
    If no rate limits are cached, queries GitHub's `/rate_limit` endpoint directly.
    """
    global _in_memory_ratelimit
    
    # 1. Try reading from Redis cache
    if redis_client:
        try:
            limit = redis_client.get("github:ratelimit:limit")
            remaining = redis_client.get("github:ratelimit:remaining")
            reset = redis_client.get("github:ratelimit:reset")
            if limit is not None and remaining is not None:
                return {
                    "limit": int(limit),
                    "remaining": int(remaining),
                    "reset": int(reset) if reset else None,
                    "source": "redis_cache"
                }
        except Exception as e:
            current_app.logger.warning(f"Failed to read rate limits from Redis: {e}")
            
    # 2. Try reading from in-memory fallback
    if _in_memory_ratelimit["limit"] is not None and _in_memory_ratelimit["remaining"] is not None:
        return {
            **_in_memory_ratelimit,
            "source": "in_memory"
        }
        
    # 3. Query GitHub directly
    token = current_app.config.get('GITHUB_TOKEN')
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    try:
        response = requests.get("https://api.github.com/rate_limit", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            core = data.get("resources", {}).get("core", {})
            limit_val = core.get("limit")
            remaining_val = core.get("remaining")
            reset_val = core.get("reset")
            
            update_rate_limits(limit_val, remaining_val, reset_val)
            
            return {
                "limit": limit_val,
                "remaining": remaining_val,
                "reset": reset_val,
                "source": "github_api_fetch"
            }
    except Exception as e:
        current_app.logger.error(f"Failed to fetch rate limits from GitHub: {e}")
        
    # Default estimation if completely offline/unconfigured
    return {
        "limit": 5000,
        "remaining": 5000,
        "reset": None,
        "source": "default_estimation"
    }
