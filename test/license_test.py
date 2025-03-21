def test_generate_license(authenticated_client, init_test_db):
    response = authenticated_client.post('/generate-license/1')
    assert response.status_code == 201
    assert 'license_key' in response.json

def test_get_licenses(authenticated_client, init_test_db):
    """Test retrieving all licenses from the /licenses endpoint with authentication."""
    # Make the GET request to /licenses with an authenticated client
    response = authenticated_client.get('/licenses')
    
    # Assertions
    assert response.status_code == 200, f"Expected 200, got {response.status_code} with response: {response.data.decode()}"
    assert 'licenses' in response.json, "Response JSON missing 'licenses' key"
    licenses = response.json['licenses']
    
    # Check that the response includes the license from init_test_db
    assert len(licenses) >= 1, "Expected at least one license in the response"
    test_license = next((l for l in licenses if l['license_key'] == 'test-license-key'), None)
    assert test_license is not None, "Test license 'test-license-key' not found in response"
    assert test_license['user_id'] == init_test_db.id, f"Expected user_id {init_test_db.id}, got {test_license['user_id']}"
    assert test_license['is_active'] is True, "Expected is_active to be True"