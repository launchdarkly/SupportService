import logging
import os
from threading import Lock

import ldclient
import redis

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_caching import Cache
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.serving import run_simple
from werkzeug.exceptions import NotFound
from flask_redis import FlaskRedis

from app.config import config
from app.util import getLdMachineUser
from app.ld import LaunchDarklyApi
from app.cli.generators import ConfigGenerator
from app.models import User
from app.db import db

import json
import pickle
import datetime

migrate = Migrate()
bootstrap =  Bootstrap()
login = LoginManager()
cache = Cache()

# Operational Feature Flags
CACHE_TIMEOUT = lambda : ldclient.get().variation('cache-timeout', getLdMachineUser(), 50)
PROJECT_NAME = 'support-service'

class CachingDisabled:
    def __call__(self):
        return ldclient.get().variation('disable-caching', getLdMachineUser(), True)

class SubdomainDispatcher(object):

    def __init__(self, debug=False, config_name='default'):
        self.lock = Lock()
        self.instances = {}
        self.ld = LaunchDarklyApi(os.environ.get('LD_API_KEY'))
        self.config_name= config_name
        if os.environ.get('TESTING') is None or os.environ.get('TESTING') == False:
            self.rclient = redis.Redis(host=os.environ.get('REDIS_HOST'))
            self.project = self.ld.get_project(PROJECT_NAME)
            project_pick = pickle.dumps(self.project)
            self.rclient.set(PROJECT_NAME, project_pick)
        else:
            import fakeredis
            self.rclient = fakeredis.FakeStrictRedis()
            self.project = {}


    def get_application(self, host):
        host = host.split(':')[0]
        logging.info(host)
        subdomain = host.split('.')[0]

        with self.lock:
            app = self.instances.get(subdomain)
            if app is None:
                app = make_app(self.ld, self.rclient, subdomain, self.project, self.config_name)
                self.instances[subdomain] = app
            return app

    def __call__(self, environ, start_response):
        app = self.get_application(environ['HTTP_HOST'])
        @login.user_loader
        def load_user(id):
            return User.query.get(id)
        return app(environ, start_response)


def create_app(env_id, env_api_key, config_name):
    """Flask application factory.

    :param config_name: Flask Configuration

    :type config_name: app.config class

    :returns: a flask application
    """
    app = Flask(__name__)
    app = build_environment(env_id, env_api_key, app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    #app.ld = ld
    app.logger.info("APP VERSION: " + app.config['VERSION'])

    bootstrap.init_app(app)
    cache.init_app(app, config=app.config['CACHE_CONFIG'])
    login.init_app(app)

    login.login_view = 'core.login'
    from app.models import AnonymousUser
    login.anonymous_user = AnonymousUser
    migrate.init_app(app, db)

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

def make_app(ld, rclient, subdomain, project, config_name):
    project = pickle.loads(rclient.get(PROJECT_NAME))
    for env in project.environments:
        if env.key == subdomain:
            return create_app(env.id, env.api_key, config_name)

    return NotFound()

def build_environment(env_id, env_api_key, app):
    if os.environ.get('TESTING') is None or os.environ.get('TESTING') == False:
        app.redis_client = FlaskRedis(app)
        logging.info(env_api_key)
        logging.info(env_id)
        app.config['LD_CLIENT_KEY'] = env_api_key
        app.config['LD_FRONTEND_KEY'] = env_id
    else:
        app.config['LD_CLIENT_KEY'] = env_id['LD_CLIENT_KEY']
        app.config['LD_FRONTEND_KEY'] = env_api_key['LD_FRONTEND_KEY']

    return app


def rundevserver(host='0.0.0.0', port=5000, domain='localhost', **options):
    """
    Modified from `flask.Flask.run`
    Runs the application on a local development server.
    :param host: the hostname to listen on. Set this to ``'0.0.0.0'`` to
                 have the server available externally as well. Defaults to
                 ``'127.0.0.1'``.
    :param port: the port of the webserver. Defaults to ``5000``
    :param domain: used to determine the subdomain
    :param options: the options to be forwarded to the underlying
                    Werkzeug server.  See
                    :func:`werkzeug.serving.run_simple` for more
                    information.
    """
    from werkzeug.serving import run_simple

    options.setdefault('use_reloader', True)
    options.setdefault('use_debugger', True)

    app = SubdomainDispatcher(config_name=os.environ.get('FLASK_ENV', 'default'))

    run_simple(host, port, app, **options)


application = SubdomainDispatcher(config_name=os.environ.get('FLASK_ENV', 'default'))


if __name__ == '__main__':
    rundevserver(host="0.0.0.0")
