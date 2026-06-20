import os
from dotenv import load_dotenv

# Load .env file from the root directory
basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-default')
    
    # Database configuration (fallback to SQLite in root if not specified)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        f'sqlite:///{os.path.join(basedir, "orbit.db")}'
    )
    # SQLAlchemy v3+ fixes some issues, but this is a standard config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis configuration
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # GitHub configuration
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    
    # Cache settings
    PROFILE_CACHE_TTL_HOURS = int(os.environ.get('PROFILE_CACHE_TTL_HOURS', 6))
    RESPONSE_CACHE_TTL_SECONDS = int(os.environ.get('RESPONSE_CACHE_TTL_SECONDS', 300))
    MAX_REPOS_FOR_LANGUAGE_DETAIL = int(os.environ.get('MAX_REPOS_FOR_LANGUAGE_DETAIL', 30))
