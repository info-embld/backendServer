from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required
from werkzeug.security import check_password_hash
from controllers.user_controller import signup, edit_user, delete_user, get_user_by_id, get_users
from models.users import User

user_bp = Blueprint('user_routes', __name__)

@user_bp.route('/signup', methods=['POST'])
def signup_route():
    try:
        if not request.json:
            return jsonify({'error': 'Missing JSON body'}), 400
        data = request.json
        required_fields = ['first_name', 'last_name', 'email', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        user_data = (data['first_name'], data['last_name'], data['email'], data['password'])
        user = signup(user_data)
        return jsonify({'message': f'User {user.first_name} {user.last_name} created'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred during signup'}), 500

@user_bp.route('/login', methods=['POST'])
def login_route():
    try:
        if not request.json:
            return jsonify({'error': 'Missing JSON body'}), 400
        data = request.json
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid email or password'}), 401
        login_user(user)
        return jsonify({'message': f'User {user.email} logged in'}), 200
    except Exception as e:
        return jsonify({'error': 'An error occurred during login'}), 500

# Edit user route
@user_bp.route('/user/edit/<int:user_id>', methods=['PUT'])
def edit_user_route(user_id):
    """Edit an existing user's information."""
    try:
        if not request.json:
            return jsonify({'error': 'Missing JSON body'}), 400
        
        data = request.json
        user_data = (user_id, data.get('first_name'), data.get('last_name'), data.get('email'), data.get('password'))
        user = edit_user(user_data)
        return jsonify({'message': f"User {user.first_name} {user.last_name}'s data edited successfully"}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400  # Changed to 400 for invalid input
    except Exception as e:
        return jsonify({'error': 'An error occurred during edit'}), 500

# Get user by ID route
@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a user by ID."""
    try:
        user = get_user_by_id(user_id)
        return jsonify({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching user'}), 500

# Get all users route
@user_bp.route('/users', methods=['GET'])
@login_required  # Restrict to logged-in users
def get_users_route():
    """Retrieve all users."""
    try:
        users = get_users()
        users_data = [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        } for user in users]
        return jsonify({'users': users_data}), 200
    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching users'}), 500

# Delete user route
@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
@login_required  # Restrict to logged-in users
def delete_user_route(user_id):
    """Delete a user by ID."""
    try:
        delete_user(user_id)
        return jsonify({'message': f'User with ID {user_id} deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred during deletion'}), 500

# Helper function for login
def get_user_by_email(email):
    """Retrieve a user by email."""
    return User.query.filter_by(email=email).first()
