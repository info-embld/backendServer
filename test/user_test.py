def test_signup(client, init_test_db):
    response = client.post('/signup', json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "password": "pass123"
    })
    print(f"Status: {response.status_code}, Response: {response.data.decode()}")
    assert response.status_code == 201
    assert response.json['message'] == 'User Jane Doe created'

def test_login(client, init_test_db):
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'testpass'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'User test@example.com logged in'

def test_get_user(authenticated_client, init_test_db):
    response = authenticated_client.get('/user/1')
    assert response.status_code == 200
    assert response.json['email'] == 'test@example.com'

def test_get_users(authenticated_client, init_test_db):
    response = authenticated_client.get('/users')
    assert response.status_code == 200
    assert len(response.json['users']) == 1

def test_edit_user(authenticated_client, init_test_db):
    response = authenticated_client.put('/user/edit/1', json={
        'first_name': 'Updated',
        'last_name': 'User'
    })
    assert response.status_code == 200
    assert "Updated User's data edited successfully" in response.json['message']

def test_delete_user(authenticated_client, init_test_db):
    response = authenticated_client.delete('/user/1')
    assert response.status_code == 200
    assert response.json['message'] == 'User with ID 1 deleted successfully'