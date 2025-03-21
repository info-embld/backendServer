from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models.db_conf import db

class License(db.Model):  # Fixed: db.Model, not db.model
    __tablename__ = 'licenses'  # Fixed: plural to match users.py relationship

    id = db.Column(db.Integer, primary_key=True)
    license_key = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)  # Changed to nullable=True
    is_active = db.Column(db.Boolean, default=True)
    paid = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<License {self.license_key}>'

