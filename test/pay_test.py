import pytest
from models.licenses import License
class MockSession:
    """Mimic a Stripe Session object with id and url attributes."""
    def __init__(self, payment_status='paid', metadata=None, amount_total=1500, session_id='cs_test_123'):
        self.id = session_id
        self.url = 'http://test.com'
        self.payment_status = payment_status
        self.metadata = metadata or {}
        self.amount_total = amount_total


def test_create_payment_session(authenticated_client, init_test_db, mocker):
    # Mock Stripe to return an object with attributes
    mocker.patch('stripe.checkout.Session.create', return_value=MockSession())
    
    # Get license ID dynamically
    with authenticated_client.application.app_context():
        license = License.query.filter_by(user_id=init_test_db.id).first()
        license_id = license.id if license else 1  # Should exist from init_test_db
    
    response = authenticated_client.post(
        f'/payment/create/{init_test_db.id}/{license_id}',
        json={'amount': 1000}
    )
    print(f"Status: {response.status_code}, Response: {response.data.decode()}")
    assert response.status_code == 200, f"Got {response.status_code}: {response.data.decode()}"
    assert 'session_id' in response.json
    assert response.json['session_id'] == 'cs_test_123'

def test_payment_success(authenticated_client, init_test_db, mocker):
    # Mock Stripe with an object
    mock_session = MockSession(
        payment_status='paid',
        metadata={'user_id': str(init_test_db.id), 'license_id': '1'},
        amount_total=1500
    )
    mocker.patch('stripe.checkout.Session.retrieve', return_value=mock_session)
    
    response = authenticated_client.get('/payment/success?session_id=cs_test_123')
    print(f"Status: {response.status_code}, Response: {response.data.decode()}")
    assert response.status_code == 200, f"Got {response.status_code}: {response.data.decode()}"
    assert response.json['message'] == 'Payment successful, license activated'

def test_check_payment(authenticated_client, mocker):
    # Mock Stripe with an object
    mock_session = MockSession(
        payment_status='paid',
        amount_total=1500,
        session_id='cs_test_123'
    )
    mocker.patch('stripe.checkout.Session.retrieve', return_value=mock_session)
    
    response = authenticated_client.get('/payment/check/cs_test_123')
    print(f"Status: {response.status_code}, Response: {response.data.decode()}")
    assert response.status_code == 200, f"Got {response.status_code}: {response.data.decode()}"
    assert response.json['payment_status'] == 'paid'