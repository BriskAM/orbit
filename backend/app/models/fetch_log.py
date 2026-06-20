from datetime import datetime, timezone
from backend.app.extensions import db

class FetchLog(db.Model):
    __tablename__ = 'fetch_log'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, index=True)
    fetch_type = db.Column(db.String(50), nullable=False)  # full | partial | refresh
    api_calls_used = db.Column(db.Integer, default=0)
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.Text)
    duration_ms = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'fetch_type': self.fetch_type,
            'api_calls_used': self.api_calls_used,
            'success': self.success,
            'error_message': self.error_message,
            'duration_ms': self.duration_ms,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
