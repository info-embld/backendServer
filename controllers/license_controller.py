import jwt  # Correct import for PyJWT
from models.licenses import License  # Import from models/licenses.py
from models.users import User  # Import from models/users.py
from models.db_conf import db  # Import db from main.py
from controllers.email_controller import send_email_confirmation, send_email_licenses
from datetime import datetime, timedelta
import os
import secrets

def generate_license(user_id):
    """Generate three licenses for a user and send a confirmation email."""
    licenses = []
    for _ in range(3):
        license = generating_license(user_id)
        licenses.append(license)
    send_email_confirmation(user_id)
    send_email_licenses(user_id, licenses)
    return licenses

def generating_license(user_id):
    """Generate a unique license key for a given user with 1-year expiration."""
    try:
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")

        payload = {
            'user_id': user_id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=365)
        }
        license_key = jwt.encode({'user_id': user_id, 'iat': datetime.utcnow(), 'exp': datetime.utcnow() + timedelta(days=365), 'nonce': secrets.token_hex(8)}, os.getenv('JWT_SECRET_KEY', 'test-jwt-secret-key'), algorithm='HS256')

        new_license = License(
            license_key=license_key,
            user_id=user_id,
            expires_at=payload['exp'],
            created_at=datetime.utcnow(),
            is_active=True
        )

        db.session.add(new_license)
        db.session.commit()
        return new_license
    except ValueError as e:
        raise e
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Failed to generate license: {str(e)}")

def validate_license(license_key):
    """Check if a license key is valid and not expired."""
    try:
        # Fetch the license from the database
        license = License.query.filter_by(license_key=license_key).first()
        if not license:
            return False

        # Decode the JWT to verify its integrity
        jwt.decode(license_key, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])

        # Check expiration
        if license.expires_at >= datetime.utcnow():
            return True
        return False  # Expired
    except jwt.ExpiredSignatureError:
        return False  # License expired
    except jwt.InvalidTokenError:
        return False  # Invalid token
    except Exception as e:
        raise ValueError(f"Failed to validate license: {str(e)}")

def get_license(license_id):
    """Retrieve a license by its ID."""
    try:
        license = License.query.get(license_id)
        if not license:
            raise ValueError("License not found")
        return license
    except ValueError as e:
        raise e
    except Exception as e:
        raise ValueError(f"Failed to fetch license: {str(e)}")

def get_licenses():
    """Retrieve all licenses from the database."""
    try:
        all_licenses = License.query.all()
        return all_licenses
    except Exception as e:
        raise ValueError(f"Failed to fetch licenses: {str(e)}")
    
def create_default_licenses(user_id):
    try:
        if user_id is None:
            raise ValueError("User ID cannot be None for license generation")
        expires_at = datetime.utcnow() + timedelta(days=14)  # Trial period
        payload = {'user_id': user_id, 'exp': expires_at.timestamp()}
        license_key = jwt.encode(payload, os.getenv('JWT_SECRET_KEY', 'default-jwt-secret-key'), algorithm='HS256')
        license = License(
            user_id=user_id,
            license_key=license_key,  # No TRIAL- prefix unless desired
            expires_at=expires_at,
            created_at=datetime.utcnow(),
            is_active=True
        )
        db.session.add(license)
        db.session.commit()
        send_email_confirmation(user_id)
        send_email_licenses(user_id, license.license_key)
        return license
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Failed to generate license: {str(e)}")
