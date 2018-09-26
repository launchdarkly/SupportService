import os

import ldclient
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache 

from app.config import config

db = SQLAlchemy()
migrate = Migrate()
bootstrap =  Bootstrap()
login = LoginManager()
cache = Cache(config={'CACHE_TYPE': 'redis'})

# Operational Feature Flags
CACHE_TIMEOUT = lambda : ldclient.get().variation('cache-timeout', {'key': 'any'}, 50)
CACHING_DISABLED = lambda : ldclient.get().variation('caching-disabled', {'key': 'any'}, False)

def create_app(config_name):
    """Flask application factory.

    :param config_name: Flask Configuration
    
    :type config_name: app.config class 

    :returns: a flask application
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    bootstrap.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    login.init_app(app)
    login.login_view = 'core.login'
    from app.models import AnonymousUser
    login.anonymous_user = AnonymousUser

    from app.routes import core
    app.register_blueprint(core)

    return app