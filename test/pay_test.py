import pytest

@pytest.mark.parametrize('user_id, license_id', [(1, 1)])
def test_create_payment(authenticated_client, init_test_db, user_id, license_id, mocker):
    mocker.patch('stripe.checkout.Session.create', return_value={
        'id': 'cs_test_123',
        'url': 'https://checkout.stripe.com/test'
    })
    response = authenticated_client.post(f'/payment/create/{user_id}/{license_id}', json={'amount': 1500})
    assert response.status_code == 200
    assert 'session_id' in response.json
    assert response.json['url'].startswith('https://checkout.stripe.com')

def test_payment_success(authenticated_client, init_test_db, mocker):
    mocker.patch('stripe.checkout.Session.retrieve', return_value={
        'payment_status': 'paid',
        'metadata': {'user_id': '1', 'license_id': '1'},
        'amount_total': 1500
    })
    response = authenticated_client.get('/payment/success?session_id=cs_test_123')
    assert response.status_code == 200
    assert response.json['message'] == 'Payment successful, license activated'

def test_check_payment(authenticated_client, mocker):
    mocker.patch('stripe.checkout.Session.retrieve', return_value={
        'id': 'cs_test_123',
        'payment_status': 'paid',
        'amount_total': 1500
    })
    response = authenticated_client.get('/payment/check/cs_test_123')
    assert response.status_code == 200
    assert response.json['payment_status'] == 'paid'