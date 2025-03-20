from flask import Blueprint, request, jsonify
from flask_login import login_required
from controllers.payments_controller import create_payment_session, process_payment, check_payment_status

payments_bp = Blueprint('payments_routes', __name__)

@payments_bp.route('/payment/create/<int:user_id>/<int:license_id>', methods=['POST'])
@login_required
def create_payment(user_id, license_id):
    try:
        amount = request.json.get('amount', 1000)
        session_data = create_payment_session(user_id, license_id, amount)
        return jsonify({
            'session_id': session_data['session_id'],
            'url': session_data['url']
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

@payments_bp.route('/payment/success', methods=['GET'])
@login_required
def payment_success():
    try:
        session_id = request.args.get('session_id')
        if not session_id:
            return jsonify({'error': 'Missing session_id parameter'}), 400
        result = process_payment(session_id)
        if result['status'] == 'success':
            return jsonify({'message': 'Payment successful, license activated'}), 200
        return jsonify({'message': 'Payment not completed'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

@payments_bp.route('/payment/check/<session_id>', methods=['GET'])
@login_required
def check_payment(session_id):
    try:
        status = check_payment_status(session_id)
        return jsonify(status), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500