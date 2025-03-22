# tests/test_email_route.py

def test_send_update_email_success(authenticated_client, init_test_db, mock_smtp):
    """Test sending an update email successfully."""
    # Make a request to an email-sending endpoint
    response = authenticated_client.post('/send-update', json={
        'subject': 'Test Update',
        'body': 'This is a test email.'
    })
    
    # Assertions
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data.decode()}"
    assert response.json['message'] == 'Email sent successfully'
    
    # Verify email was "sent" via mock
    mock_smtp.return_value.sendmail.assert_called_once()