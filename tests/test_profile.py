def test_get_profile(client):
    # First, register and login to get a token
    client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    })
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'password'
    })
    access_token = response.json['access_token']

    # Test accessing profile
    response = client.get('/profile', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert b'Profile info' in response.data
