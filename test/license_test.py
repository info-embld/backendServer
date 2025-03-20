def test_generate_license(authenticated_client, init_test_db):
    response = authenticated_client.post('/generate-license/1')
    assert response.status_code == 201
    assert 'license_key' in response.json

def test_validate_license(authenticated_client, init_test_db, mocker):
    mocker.patch('jwt.decode', return_value={'user_id': 1, 'exp': 9999999999})
    response = authenticated_client.post('/validate-license', json={
        'license_key': 'mocked_jwt_token'
    })
    assert response.status_code == 200
    assert response.json['valid'] is True