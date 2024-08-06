class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    JWT_SECRET_KEY = 'your_test_secret_key'
