import os
import ldclient

class Config(object):
    """Base Config"""
    VERSION = '1.0.2'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    # LaunchDarkly
    ldclient.set_sdk_key(os.environ.get("LD_CLIENT_KEY"))

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Configuration used for local development."""
    DEBUG = True 

    @staticmethod
    def init_app(app):
        Config.init_app(app)

        with app.app_context():
            from app.factory import db
            from app.models import User

            db.init_app(app)


class TestingConfig(Config):
    """Configuration used for testing and CI."""
    TESTING = True 
    DEBUG = True 

    @staticmethod
    def init_app(app):
        Config.init_app(app)

        with app.app_context():
            from app.factory import db 
            from app.models import User

            db.init_app(app)
            db.create_all()

            from ldclient.config import Config as __config
            ldclient.set_config(__config(offiline=True))


class ProductionConfig(Config):
    """Configuration used for production environments."""

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}