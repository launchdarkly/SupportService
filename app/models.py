import hashlib
import uuid
import time

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.factory import db, login


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #account_types = Personal, Professional, Business, Premium
    account_type = db.Column(db.String(120), default='Business')
    user_type = db.Column(db.String(120), default='Beta')
    state = db.Column(db.String(120), default='Ca')
    country = db.Column(db.String(120), default='USA')
    set_path = db.Column(db.String(120), default='default')


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_email_hash(self):
        return hashlib.md5(self.email.encode()).hexdigest()

    def get_ld_user(self, random=None):
        app_version = current_app.config['VERSION']
        millis = int(round(time.time() * 1000))

        if random:
            user_key = str(uuid.uuid1())
        else:
            user_key = self.get_email_hash()

        user = {
            'key': user_key,
            'email': self.email,
            "custom": {
                'account_type': self.account_type,
                'user_type': self.user_type,
                'state': self.state,
                'country': self.country,
                'app_version': app_version,
                'date': millis
            },
            'privateAttributes': ['account_type', 'state'],
        }
        return user

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class AnonymousUser(AnonymousUserMixin):

    def __init__(self):
        super(AnonymousUserMixin, self).__init__()

    def get_ld_user(self):
        app_version = current_app.config['VERSION']
        user = {
            "key": "anonymous",
            "custom": {
                "app_version": app_version
            },
            "anomymous": True
        }

        return user