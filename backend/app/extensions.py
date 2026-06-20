from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import redis
import logging

db = SQLAlchemy()
migrate = Migrate()

# Global redis client placeholder
redis_client = None

def init_redis(app):
    global redis_client
    redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
    try:
        # Attempt to initialize and ping Redis
        client = redis.Redis.from_url(redis_url, decode_responses=True)
        client.ping()
        redis_client = client
        app.logger.info("Redis connection established successfully.")
    except Exception as e:
        app.logger.warning(
            f"Redis connection failed (URL: {redis_url}): {e}. "
            "Proceeding without Redis cache."
        )
        redis_client = None
