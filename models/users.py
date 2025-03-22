from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta
from models.db_conf import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    subbed = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    newsletter_sub = db.Column(db.Boolean, default=True)
    address = db.Column(db.String(256), nullable=True)

    licenses = db.relationship('License', backref='user', lazy=True)

    def __init__(self, **kwargs):
        """Initialize a new user."""
        super(User, self).__init__(**kwargs)

    def get_id(self):
        """Return the user ID as a string for Flask-Login."""
        return str(self.id)
    
    def __repr__(self):
        """String representation of the user."""
        return f'<User {self.email}>'
    
    def get_username(self):
        """Return the full name of the user."""
        return f'{self.first_name} {self.last_name}'
