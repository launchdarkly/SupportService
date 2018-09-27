import logging
import os

import ldclient
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_caching import Cache
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

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

    @app.before_request
    def set_logging_level():
        """Set Logging Level Based on Feature Flag

        This uses LaunchDarkly to update the logging level dynamically.
        Before each request runs, we check the current logging level and
        it does not match, we update it to the new value.

        Logging levels are integer values based on the standard Logging library
        in python: https://docs.python.org/3/library/logging.html#logging-levels 

        This is an operational feature flag.
        """
        logLevel = ldclient.get().variation("set-logging-level", {"key": "any"}, logging.INFO)

        app.logger.info("Log level is {0}".format(logLevel))

        # set app 
        app.logger.setLevel(logLevel)
        # set werkzeug
        logging.getLogger('werkzeug').setLevel(logLevel)
        # set root
        logging.getLogger().setLevel(logLevel)
        
    return app
