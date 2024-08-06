# Example fix in tests/test_art.py
def test_add_artwork(client):
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
    
    # Add an artwork
    response = client.post('/artworks', json={
        'title': 'New Artwork',
        'description': 'Description of the artwork',
        'price': 100.0,
        'artist_id': 1  # Add this key if your route requires it
    }, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 201
