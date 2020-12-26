import os


class BaseConfig:
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0
    TOKEN_EXPIRATION_SECONDS = 3
