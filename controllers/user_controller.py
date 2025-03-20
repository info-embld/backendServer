from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from models.users import User  # Import from models/users.py
from models.db_conf import db  # Import db from main.py

# Signup function
def signup(user_data):
    """Create a new user with the provided data."""
    try:
        first_name, last_name, email, password = user_data  # Unpack tuple/list
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already registered")

        # Hash the password with Werkzeug
        password_hash = generate_password_hash(password, method='sha256')

        # Create new user instance (this triggers 3 trial licenses via User.__init__)
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password_hash
        )

        # Add to database and commit
        db.session.add(new_user)
        db.session.commit()

        # Optionally log the user in after signup
        login_user(new_user)
        return new_user
    except ValueError as e:
        raise e
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Signup failed: {str(e)}")

# Get all users
def get_users():
    """Retrieve all users from the database."""
    try:
        users = User.query.all()
        return users
    except Exception as e:
        raise ValueError(f"Failed to fetch users: {str(e)}")

# Get user by ID
def get_user_by_id(user_id):
    """Retrieve a user by their ID."""
    try:
        user = User.query.get(int(user_id))  # Convert to int for safety
        if not user:
            raise ValueError("User not found")
        return user
    except ValueError as e:
        raise e
    except Exception as e:
        raise ValueError(f"Failed to fetch user: {str(e)}")

# Edit user
def edit_user(user_data):
    """Update an existing user's information."""
    try:
        user_id, first_name, last_name, email, password = user_data  # Unpack data
        
        # Fetch the user
        user = User.query.get(int(user_id))
        if not user:
            raise ValueError("User not found")

        # Update fields if provided (enforce non-null for first_name and last_name)
        if first_name is not None:  # Only update if provided, but don’t allow None
            user.first_name = first_name
        elif not user.first_name:  # Ensure it’s not null after update
            raise ValueError("First name cannot be empty")
        if last_name is not None:
            user.last_name = last_name
        elif not user.last_name:
            raise ValueError("Last name cannot be empty")
        if email and email != user.email:
            # Check if new email is already taken
            if User.query.filter_by(email=email).first():
                raise ValueError("Email already in use")
            user.email = email
        if password:
            user.password_hash = generate_password_hash(password, method='sha256')

        # Commit changes
        db.session.commit()
        return user
    except ValueError as e:
        db.session.rollback()
        raise e
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Edit failed: {str(e)}")

# Delete user
def delete_user(user_id):
    """Delete a user by their ID."""
    try:
        user = User.query.get(int(user_id))
        if not user:
            raise ValueError("User not found")
        
        db.session.delete(user)
        db.session.commit()
        return True
    except ValueError as e:
        raise e
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Delete failed: {str(e)}")