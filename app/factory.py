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
from app.util import getLdMachineUser

db = SQLAlchemy()
migrate = Migrate()
bootstrap =  Bootstrap()
login = LoginManager()
cache = Cache(config={'CACHE_TYPE': 'redis'})

# Operational Feature Flags
CACHE_TIMEOUT = lambda : ldclient.get().variation('cache-timeout', getLdMachineUser(), 50)

class CachingDisabled:
    def __call__(self):
        return ldclient.get().variation('caching-disabled', getLdMachineUser(), False)

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
    def setLoggingLevel():
        """Set Logging Level Based on Feature Flag

        This uses LaunchDarkly to update the logging level dynamically.
        Before each request runs, we check the current logging level and
        it does not match, we update it to the new value.

        Logging levels are integer values based on the standard Logging library
        in python: https://docs.python.org/3/library/logging.html#logging-levels 

        This is an operational feature flag.
        """
        from flask import request
        logLevel = ldclient.get().variation("set-logging-level", getLdMachineUser(request), logging.INFO)

        app.logger.info("Log level is {0}".format(logLevel))

        # set app 
        app.logger.setLevel(logLevel)
        # set werkzeug
        logging.getLogger('werkzeug').setLevel(logLevel)
        # set root
        logging.getLogger().setLevel(logLevel)
        
    return app
