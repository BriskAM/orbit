from datetime import datetime, timezone
from backend.app.extensions import db

class CachedProfile(db.Model):
    __tablename__ = 'cached_profile'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    display_name = db.Column(db.String(150))
    avatar_url = db.Column(db.String(500))
    bio = db.Column(db.Text)
    company = db.Column(db.String(150))
    location = db.Column(db.String(150))
    blog_url = db.Column(db.String(500))
    twitter_username = db.Column(db.String(100))
    follower_count = db.Column(db.Integer, default=0)
    following_count = db.Column(db.Integer, default=0)
    public_repo_count = db.Column(db.Integer, default=0)
    account_created_at = db.Column(db.DateTime)
    total_stars_earned = db.Column(db.Integer, default=0)
    total_forks_received = db.Column(db.Integer, default=0)
    total_commits_last_year = db.Column(db.Integer, default=0)
    longest_streak_days = db.Column(db.Integer, default=0)
    current_streak_days = db.Column(db.Integer, default=0)
    top_language = db.Column(db.String(100))
    language_breakdown = db.Column(db.JSON)  # stores dict of languages and their percentages
    metrics_json = db.Column(db.JSON)        # full calculated metrics JSON
    last_fetched_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    fetch_count = db.Column(db.Integer, default=1)
    
    # Relationship to RepoSnapshot
    repos = db.relationship('RepoSnapshot', backref='profile', lazy=True, cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'display_name': self.display_name,
            'avatar_url': self.avatar_url,
            'bio': self.bio,
            'company': self.company,
            'location': self.location,
            'blog_url': self.blog_url,
            'twitter_username': self.twitter_username,
            'follower_count': self.follower_count,
            'following_count': self.following_count,
            'public_repo_count': self.public_repo_count,
            'account_created_at': self.account_created_at.isoformat() if self.account_created_at else None,
            'total_stars_earned': self.total_stars_earned,
            'total_forks_received': self.total_forks_received,
            'total_commits_last_year': self.total_commits_last_year,
            'longest_streak_days': self.longest_streak_days,
            'current_streak_days': self.current_streak_days,
            'top_language': self.top_language,
            'language_breakdown': self.language_breakdown,
            'metrics_json': self.metrics_json,
            'last_fetched_at': self.last_fetched_at.isoformat() if self.last_fetched_at else None,
            'fetch_count': self.fetch_count
        }
