from backend.app.extensions import db

class RepoSnapshot(db.Model):
    __tablename__ = 'repo_snapshot'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('cached_profile.id'), nullable=False)
    repo_name = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text)
    is_fork = db.Column(db.Boolean, default=False)
    primary_language = db.Column(db.String(100))
    languages_json = db.Column(db.JSON)  # byte breakdown for this repo
    stars = db.Column(db.Integer, default=0)
    forks = db.Column(db.Integer, default=0)
    watchers = db.Column(db.Integer, default=0)
    open_issues = db.Column(db.Integer, default=0)
    size_kb = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime)
    pushed_at = db.Column(db.DateTime)
    topics = db.Column(db.JSON)  # list of tags/topics
    
    def to_dict(self):
        return {
            'id': self.id,
            'repo_name': self.repo_name,
            'full_name': self.full_name,
            'description': self.description,
            'is_fork': self.is_fork,
            'primary_language': self.primary_language,
            'languages_json': self.languages_json,
            'stars': self.stars,
            'forks': self.forks,
            'watchers': self.watchers,
            'open_issues': self.open_issues,
            'size_kb': self.size_kb,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'pushed_at': self.pushed_at.isoformat() if self.pushed_at else None,
            'topics': self.topics
        }
