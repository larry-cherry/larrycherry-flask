from os import getenv, environ

class Config(object):
    DEBUG = False
    TESTING = False
    # DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    SITE_ROOT_URL = getenv('SITE_ROOT_URL')
    EXAMPLE = 'ProductionConfig Testing'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)

class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SITE_ROOT_URL = 'http://127.0.0.1:5000/'
    SEND_FILE_MAX_AGE_DEFAULT = 0
    SQLALCHEMY_DATABASE_URI = 'postgres://postgresdev:password@localhost:5432/flask'
    # environ['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'This is a secret'


class TestingConfig(Config):
    SITE_ROOT_URL = 'http://127.0.0.1:5555/'
    TESTING = True


def get_config():
    flask_env = getenv('FLASK_ENV')
    if flask_env == 'production':
        return 'configs.ProductionConfig'
    elif flask_env == 'development':
        return 'configs.DevelopmentConfig'
    elif flask_env == 'testing':
        return 'configs.TestingConfig'
    else:
        raise Exception('FLASK_ENV is not set')
        return 'configs.DevelopmentConfig'
