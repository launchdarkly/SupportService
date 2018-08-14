from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import ldclient
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

ldclient.set_sdk_key(os.getenv("LD_CLIENT_KEY"))
#ldclient.set_config(ldclient.Config(sdk_key='sdk-8929dfb7-7edd-4bec-9856-db3bd80a6661', stream_uri="18.236.106.41:8030"))
ld_client = ldclient.get()

from app import routes, models
