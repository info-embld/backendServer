from flask import Blueprint, request, jsonify, current_app
from controllers.email_controller import send_update_email

email_bp = Blueprint('email_route', __name__)

@email_bp.route('/send-update', methods=['POST'])
def send_update_route():
    try:
        data = request.json
        subject = data.get('subject', 'Newsletter Update')
        message = data.get('message', 'No message provided.')
        result = send_update_email(subject, message, current_app.mail)  # Pass mail instance
        if result is None:
            return jsonify({'message': 'No subscribed users'}), 200
        return jsonify({'message': 'Emails sent to subscribed users'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 500
