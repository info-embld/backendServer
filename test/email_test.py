# tests/test_email_route.py
from flask_mail import Mail

def test_send_update_email_success(authenticated_client, init_test_db, app):
    with app.mail.record_messages() as outbox:
        response = authenticated_client.post('/send-update', json={
            'subject': 'Test Update',
            'message': 'This is a test message'
        })
        assert response.status_code == 200
        assert response.json['message'] == 'Emails sent to subscribed users'
        assert len(outbox) == 1
        assert outbox[0].subject == 'Test Update'
        assert outbox[0].recipients == ['test@example.com']