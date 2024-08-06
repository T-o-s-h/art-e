# Example fix in tests/test_comments.py
def test_post_comment(client):
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
    
    # Post a comment
    response = client.post('/comments', json={
        'content': 'Great artwork!',
        'artwork_id': 1
    }, headers={'Authorization': f'Bearer {access_token}'})
    
    assert response.status_code == 201
    assert b'{"message":"Comment created"}' in response.data
