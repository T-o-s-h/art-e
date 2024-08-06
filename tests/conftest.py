import pytest
from flask_migrate import Migrate, upgrade
from app import create_app, db

@pytest.fixture(scope='module')
def app():
    """Create a Flask app instance for testing."""
    app = create_app(config_name='config.TestingConfig')

    with app.app_context():
        # Apply migrations before yielding the app
        upgrade()
        yield app

        # Clean up after tests
        db.session.remove()
        db.drop_all()

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
    return Migrate(app, db)
