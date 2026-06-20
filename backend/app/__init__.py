from flask import Flask
from flask_cors import CORS
from backend.app.config import Config
from backend.app.extensions import db, migrate, init_redis

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configure CORS - allows frontend connections
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize Flask Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    init_redis(app)
    
    # Import models to ensure SQLAlchemy registers them
    from backend.app.models.profile import CachedProfile
    from backend.app.models.repo_snapshot import RepoSnapshot
    from backend.app.models.fetch_log import FetchLog
    
    # Register Blueprints
    from backend.app.api.profile import profile_bp
    app.register_blueprint(profile_bp)
    
    from backend.app.api.meta import meta_bp
    app.register_blueprint(meta_bp)
    
    # Automatically create tables for ease of development
    with app.app_context():
        try:
            db.create_all()
            app.logger.info("Database tables verified/created successfully.")
        except Exception as e:
            app.logger.error(f"Error initializing database tables: {e}")
            
    return app
