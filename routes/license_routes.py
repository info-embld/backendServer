from flask import Blueprint, request, jsonify
from flask_login import login_required  # Add this import
from controllers.license_controller import generate_license, validate_license, get_licenses

license_bp = Blueprint('license_routes', __name__)

@license_bp.route('/generate-license/<int:user_id>', methods=['POST'])
@login_required
def generate_license_route(user_id):
    try:
        license = generate_license(user_id)
        return jsonify({'license_key': license.license_key}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

@license_bp.route('/validate-license', methods=['POST'])
@login_required
def validate_license_route():
    try:
        if not request.json or 'license_key' not in request.json:
            return jsonify({'error': 'Missing license_key in request body'}), 400
        license_key = request.json.get('license_key')
        is_valid = validate_license(license_key)
        return jsonify({'valid': is_valid}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500
    
@license_bp.route('/licenses', methods=['GET'])
@login_required
def get_licenses_route():
    """Retrieve all licenses from the database."""
    try:
        licenses = get_licenses()
        # Convert licenses to a JSON-serializable format
        licenses_data = [{
            'id': license.id,
            'license_key': license.license_key,
            'user_id': license.user_id,
            'created_at': license.created_at.isoformat(),
            'expires_at': license.expires_at.isoformat() if license.expires_at else None,
            'is_active': license.is_active
        } for license in licenses]
        return jsonify({'licenses': licenses_data}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"An error occurred while fetching licenses: {str(e)}"}), 500