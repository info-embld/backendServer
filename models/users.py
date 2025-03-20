from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta
from models.licenses import License  # Import License model for creating default licenses
from models.db_conf import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    newsletter_sub = db.Column(db.Boolean, default=False)

    licenses = db.relationship('License', backref='user', lazy=True)

    def __init__(self, **kwargs):
        """Initialize a new user and create 3 default trial licenses."""
        super(User, self).__init__(**kwargs)
        # Create 3 trial licenses when a new user is created
        self.create_default_licenses()

    def create_default_licenses(self):
        """Create 3 licenses with a 14-day free trial for the user."""
        for _ in range(3):
            trial_license = License(
                user_id=self.id,
                license_key=f"TRIAL-{self.id}-{_}",  # Simple trial key; replace with JWT if needed
                expires_at=datetime.utcnow() + timedelta(days=14),  # 14-day trial
                is_active=True
            )
            db.session.add(trial_license)

    def get_id(self):
        """Return the user ID as a string for Flask-Login."""
        return str(self.id)
    
    def __repr__(self):
        """String representation of the user."""
        return f'<User {self.email}>'
    
    def get_username(self):
        """Return the full name of the user."""
        return f'{self.first_name} {self.last_name}'
