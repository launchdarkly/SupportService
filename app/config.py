import logging
import os
import subprocess
import sys

import ldclient
from ldclient import Config as LdConfig

log = logging.getLogger()

def env_var(key, default=None, required=False):
    """
    Helper function to parse environment variables.
    """
    if default is not None:
        var = os.environ.get(key, default)
    elif required:
        try:
            var = os.environ[key]
        except KeyError:
            log.error("ERROR: Required Environment Variable {0} is not set.".format(key))
        if len(os.environ[key]) == 0:
            log.error("ERROR: Required Environment Variable {0} is empty".format(key))

    try:
        return var
    except UnboundLocalError as ex:
        log.error("ERROR: {0}".format(ex))


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
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    CACHE_REDIS_HOST = REDIS_HOST
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_CONFIG = {'CACHE_TYPE': 'simple'}

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Configuration used for local development."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///supportservice.db"

    @staticmethod
    def init_app(app):
        Config.init_app(app)
        with app.app_context():

            from app.db import db
            from app.models import User
            from app.models import Plan

            db.init_app(app)
            db.create_all()

            # check if plans exist
            if len(Plan.query.all()) != 4:
                p1 = Plan(id=1, name='free', description='All the basic features of SupportService', cost=0)
                db.session.add(p1)
                p2 = Plan(id=2, name='bronze', description='Everything in free and email support.', cost=25)
                db.session.add(p2)
                p3 = Plan(id=3, name='silver', description='Everything in bronze and chat support.', cost=50)
                db.session.add(p3)
                p4 = Plan(id=4, name='gold', description='Everything in silver and 99.999% uptime SLA!', cost=50)
                db.session.add(p4)
                db.session.commit()

            # check if user exists
            if User.query.filter_by(email='test@tester.com').first() is None:
                app.logger.info("Creating test user: test@tester.com password: test")
                u = User(email='test@tester.com')
                u.set_password('test')
                db.session.add(u)
                db.session.commit()
            else:
                app.logger.info("You can login with user: test@tester.com password: test")

class TestingConfig(Config):
    """Configuration used for testing and CI."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///supportservice.db"

    @staticmethod
    def init_app(app):
        Config.init_app(app)

        with app.app_context():
            from app.db import db
            from app.models import User

            db.init_app(app)
            db.create_all()

            from ldclient.config import Config as __config
            ldclient.set_config(__config(offline=True))


class StagingConfig(Config):
    """Configuration used for production environments."""
    CACHE_CONFIG = {'CACHE_TYPE': 'redis'}

    @staticmethod
    def init_app(app):
        Config.init_app(app)
        with app.app_context():
            from app.db import db
            from app.models import User
            from app.models import Plan

            db.init_app(app)


class ProductionConfig(Config):
    """Configuration used for production environments."""
    CACHE_CONFIG = {'CACHE_TYPE': 'redis'}

    @staticmethod
    def init_app(app):
        Config.init_app(app)
        with app.app_context():
            from app.db import db
            from app.models import User
            from app.models import Plan

            db.init_app(app)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'staging': StagingConfig,
    'default': DevelopmentConfig
}
