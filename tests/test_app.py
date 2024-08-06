import pytest
from flask import url_for
from app import create_app, db

@pytest.fixture(scope='module')
def app():
    """Create a Flask app instance for testing."""
    app = create_app(config_name='config.TestingConfig')  # Ensure 'TestingConfig' is defined in your app
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture(scope='module')
def runner(app):
    """Create a test runner for running CLI commands."""
    return app.test_cli_runner()

@pytest.fixture(scope='module')
def migrate(app):
    """Create a Migrate instance for testing."""
    from flask_migrate import Migrate
    migrate = Migrate(app, db)
    return migrate

def test_home_page(client):
    """Test the home page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Art Gallery' in response.data

def test_custom_404(client):
    """Test the custom 404 page."""
    response = client.get('/nonexistentpage')
    assert response.status_code == 404
    assert b'Welcome to Art Gallery' in response.data

# Optionally add more tests for other endpoints or features as needed
