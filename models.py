from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin' or 'event_manager'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    events = db.relationship('Event', backref='creator', lazy=True)
    activity_logs = db.relationship('ActivityLog', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash and store password"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user has admin role"""
        return self.role == 'admin'


class Cluster(db.Model):
    __tablename__ = 'clusters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    logo_filename = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    participants = db.relationship('Participant', backref='cluster', lazy=True)
    
    def get_total_points(self):
        """Calculate sum of all participant points for this cluster"""
        total = db.session.query(db.func.sum(Participant.points))\
            .filter(Participant.cluster_id == self.id)\
            .scalar()
        return total or 0
    
    def get_logo_url(self):
        """Return URL to logo image"""
        if self.logo_filename:
            return f'/static/images/clusters/{self.logo_filename}'
        return f'/static/images/clusters/{self.name.lower()}.png'


class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    participants = db.relationship('Participant', backref='event', lazy=True, cascade='all, delete-orphan')
    
    def get_participants_by_cluster(self):
        """Group participants by cluster"""
        result = {}
        for participant in self.participants:
            cluster_name = participant.cluster.name
            if cluster_name not in result:
                result[cluster_name] = {
                    'cluster': participant.cluster,
                    'participants': []
                }
            result[cluster_name]['participants'].append(participant)
        return result
    
    def get_creator(self):
        """Return User object who created event"""
        return User.query.get(self.created_by)


class Participant(db.Model):
    __tablename__ = 'participants'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    cluster_id = db.Column(db.Integer, db.ForeignKey('clusters.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(Participant, self).__init__(**kwargs)
        # Validate constraints
        if self.points is not None and self.points < 0:
            raise ValueError("Points must be >= 0")
        if self.position is not None and self.position < 1:
            raise ValueError("Position must be >= 1")


class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    details = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_user(self):
        """Return User object"""
        return User.query.get(self.user_id)
    
    def get_details_dict(self):
        """Parse JSON details to dictionary"""
        if self.details:
            try:
                return json.loads(self.details)
            except json.JSONDecodeError:
                return {}
        return {}
