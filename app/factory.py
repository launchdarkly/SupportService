import logging
import os
from threading import Lock
import pickle

import ldclient
from ldclient import Config as LdConfig
from ldclient.feature_store import CacheConfig, InMemoryFeatureStore
from ldclient.integrations import Redis

import redis

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.serving import run_simple
from werkzeug.exceptions import NotFound
from flask_redis import FlaskRedis
from flask_caching import Cache
from app.config import config
from app.util import getLdMachineUser
from app.ld import LaunchDarklyApi
from app.cli.generators import ConfigGenerator
from app.db import db

migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()
cache = Cache()

PROJECT_NAME = os.environ.get("LD_PROJECT_NAME", "support-service")


class SubdomainDispatcher(object):
    def __init__(self, debug=False, config_name="default"):
        self.lock = Lock()
        self.instances = {}
        self.ld = LaunchDarklyApi(os.environ.get("LD_API_KEY"))
        self.config_name = config_name
        if os.environ.get("TESTING") is None or os.environ.get("TESTING") == False:
            self.rclient = redis.Redis(host=os.environ.get("REDIS_HOST"))
        else:
            import fakeredis

            self.rclient = fakeredis.FakeStrictRedis()

    def get_application(self, host):
        host = host.split(":")[0]
        logging.info(host)
        subdomain = host.split(".")[0]

        with self.lock:
            # Check if flask already has instance in memory
            app = self.instances.get(subdomain)
            # If not, make new instance
            if app is None:
                app = make_app(self.ld, self.rclient, subdomain, self.config_name)
                # If environment does not exist in Redis
                if app is None:
                    return NotFound()
                else:
                    self.instances[subdomain] = app
            return app

    def __call__(self, environ, start_response):
        app = self.get_application(environ["HTTP_HOST"])

        @login.user_loader
        def load_user(id):
            from app.models import User

            return User.query.get(id)

        return app(environ, start_response)


def create_app(env_id, env_api_key, config_name):
    """Flask application factory.

    :param env_id: LD Environment SDK Key

    :type env_id: string

    :param env_api_key: LD Environment Client ID

    :type env_api_key: string

    :param config_name: Flask Configuration

    :type config_name: app.config class

    :returns: a flask application
    """

    app = Flask(__name__)
    if env_api_key:
        app.config["LD_CLIENT_KEY"] = env_api_key
        logging.info(env_api_key)
    if env_id:
        app.config["LD_FRONTEND_KEY"] = env_id
        logging.info(env_id)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app = build_environment(app)
    app.ldclient = setup_ld_client(app)
    app.logger.info("APP VERSION: " + app.config["VERSION"])

    bootstrap.init_app(app)
    flask_cache_key = env_id + "-flask-"
    cache_config = {**app.config["CACHE_CONFIG"], "CACHE_KEY_PREFIX": flask_cache_key}
    cache.init_app(app, config=cache_config)
    login.init_app(app)

    login.login_view = "core.login"
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

        logLevel = app.ldclient.variation(
            "set-logging-level", getLdMachineUser(request), logging.INFO
        )

        app.logger.info("Log level is {0}".format(logLevel))

        # set app
        app.logger.setLevel(logLevel)
        # set werkzeug
        logging.getLogger("werkzeug").setLevel(logLevel)
        # set root
        logging.getLogger().setLevel(logLevel)

    return app


def make_app(ld, rclient, subdomain, config_name):
    """Check for LD Environment and build app
    :param ld: Launchdarkly API Client

    :type ld: launchdarkly_api class

    :param rclient: Redis client

    :type rclient: Redis client

    :param subdomain: URL subdomain

    :type subdomain: string

    :param config_name: Flask Configuration

    :type config_name: app.config class

    :returns: Flask application
    """
    load_project = rclient.get(PROJECT_NAME)
    if load_project is None:
        project = ld.get_project(PROJECT_NAME)
        rclient.set(PROJECT_NAME, pickle.dumps(project))
    else:
        project = pickle.loads(load_project)

    for env in project.environments:
        if env.key == subdomain:
            return create_app(env.id, env.api_key, config_name)

    return None


def setup_ld_client(app):
    # define and set required env vars
    redis_prefix = app.config["LD_FRONTEND_KEY"] + "-featurestore"
    redis_conn = "redis://" + app.config["REDIS_HOST"] + ":6379"
    if os.environ.get("TESTING") is None or os.environ.get("TESTING") == False:
        store = Redis.new_feature_store(
            url=redis_conn, prefix=redis_prefix, caching=CacheConfig.disabled()
        )
    elif os.environ.get("FLASK_ENV") == "default":
        store = InMemoryFeatureStore()
    else:
        store = InMemoryFeatureStore()

    LD_CLIENT_KEY = app.config["LD_CLIENT_KEY"]
    LD_FRONTEND_KEY = app.config["LD_FRONTEND_KEY"]
    ld_config = LdConfig(
        sdk_key=LD_CLIENT_KEY, connect_timeout=30, read_timeout=30, feature_store=store, inline_users_in_events=True
    )

    # LaunchDarkly Config
    # If $LD_RELAY_URL is set, client will be pointed to a relay instance.
    if "LD_RELAY_URL" in os.environ:
        base_uri = os.environ.get("LD_RELAY_URL")
        ld_config = LdConfig(
            sdk_key=app.config["LD_CLIENT_KEY"],
            base_uri=base_uri,
            events_uri=os.environ.get("LD_RELAY_EVENTS_URL", base_uri),
            stream_uri=os.environ.get("LD_RELAY_STREAM_URL", base_uri),
        )

    new_client = ldclient.LDClient(config=ld_config)

    return new_client


def build_environment(app):
    if os.environ.get("TESTING") is None or os.environ.get("TESTING") == False:
        app.redis_client = FlaskRedis(app)
    return app


def rundevserver(host="0.0.0.0", port=5000, domain="localhost", **options):
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

    options.setdefault("use_reloader", True)
    options.setdefault("use_debugger", True)

    app = SubdomainDispatcher(config_name=os.environ.get("FLASK_ENV", "default"))

    run_simple(host, port, app, **options)


application = SubdomainDispatcher(config_name=os.environ.get("FLASK_ENV", "default"))


if __name__ == "__main__":
    rundevserver(host="0.0.0.0")
