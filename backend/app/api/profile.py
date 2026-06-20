from flask import Blueprint, jsonify
from backend.app.services.github_graphql import fetch_github_profile_raw

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/api/profile/<username>', methods=['GET'])
def get_profile(username):
    """
    Fetches the profile for the given username.
    Day 1 Implementation: Directly queries GitHub GraphQL API and returns raw payload.
    """
    try:
        user_data = fetch_github_profile_raw(username)
        if user_data is None:
            return jsonify({"error": f"GitHub user '@{username}' not found"}), 404
            
        return jsonify({
            "status": "success",
            "source": "github_api",
            "cached": False,
            "data": user_data
        })
    except ValueError as e:
        return jsonify({
            "status": "error",
            "error": "Configuration Error",
            "message": str(e)
        }), 500
    except IOError as e:
        return jsonify({
            "status": "error",
            "error": "GitHub API Error",
            "message": str(e)
        }), 502
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": "Internal Server Error",
            "message": str(e)
        }), 500

@profile_bp.route('/api/health', methods=['GET'])
def health_check():
    """
    Basic health check returning API status and token configuration.
    """
    from flask import current_app
    has_token = bool(current_app.config.get('GITHUB_TOKEN'))
    return jsonify({
        "status": "healthy",
        "github_token_configured": has_token
    })
