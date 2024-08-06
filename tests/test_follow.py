import pytest
from flask_jwt_extended import create_access_token
from app import create_app, db
from app.models import User

@pytest.fixture(scope='module')
def app():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def auth_token(client):
    # Register a user
    client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    })
    
    # Register an artist
    client.post('/register', json={
        'username': 'artistuser',
        'email': 'artist@example.com',
        'password': 'password',
        'is_artist': True
    })

    # Log in to get a token
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'password'
    })
    access_token = response.json['access_token']
    return access_token

def test_follow_artist(client, auth_token):
    # Follow an artist
    response = client.post('/follow/1', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    assert b'Followed artist' in response.data

def test_get_following(client, auth_token):
    # Fetch following
    response = client.get('/following', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    assert b'following' in response.data
