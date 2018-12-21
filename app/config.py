import os
import subprocess
import ldclient
import logging
import sys
from ldclient import Config as LdConfig

class Config(object):
    """Base Config"""
    # VERSION refers to the latest git SHA1
    VERSION = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode('utf-8').rstrip()
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://{0}:{0}@{1}/{0}'.format(
            'supportService',
            'localhost'
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    CACHE_REDIS_HOST = os.environ.get('REDIS_HOST') or 'cache'

    # LaunchDarkly Config
    # If $LD_RELAY_URL is set, client will be pointed to a relay instance.
    if "LD_RELAY_URL" in os.environ:
        config = LdConfig(
            sdk_key = os.environ.get("LD_CLIENT_KEY"),
            base_uri = os.environ.get("LD_RELAY_URL"),
            events_uri = os.environ.get("LD_RELAY_URL"),
            stream_uri = os.environ.get("LD_RELAY_URL")
            enable-threads = true
        )
        ldclient.set_config(config)
    else:
        ldclient.set_sdk_key(os.environ.get("LD_CLIENT_KEY"))

    LD_FRONTEND_KEY = os.environ.get("LD_FRONTEND_KEY")

    root = logging.getLogger()
    root.setLevel(logging.INFO)

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
            ldclient.set_config(__config(offline=True))


class ProductionConfig(Config):
    """Configuration used for production environments."""

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
