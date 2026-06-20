from flask import Blueprint, Response, current_app
from backend.app.models.profile import CachedProfile
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
