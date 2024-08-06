import pytest
from app import create_app, db
from flask_jwt_extended import create_access_token

@pytest.fixture(scope='module')
def app():
    app = create_app(config_name='config.TestingConfig')  # Use config_name here
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_db(app):
    db.create_all()
    yield
    db.drop_all()

def test_register(client):
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    })
    assert response.status_code == 201
    assert b'User created' in response.data

def test_login(client):
    client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    })
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'password'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
