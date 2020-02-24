import hashlib
import time
import uuid
from datetime import datetime

from faker import Faker
from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import db

fake = Faker()

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #account_types = Personal, Professional, Business, Premium
    account_type = db.Column(db.String(120), default='Business')
    user_type = db.Column(db.String(120), default='Beta')
    state = db.Column(db.String(120), default=fake.state_abbr())
    country = db.Column(db.String(120), default=fake.country_code(representation="alpha-2"))
    set_path = db.Column(db.String(120), default='default')
    company = db.Column(db.String(255), default=fake.company())
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'), default=1)

    plan = db.relationship("Plan", backref="user", lazy="subquery")

    def _set_default_plan(self):
        return Plan.query.filter_by(name='free').first()

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_email_hash(self):
        return hashlib.md5(self.email.encode()).hexdigest()

    def get_ld_user(self):
        app_version = current_app.config['VERSION']
        milliseconds = int(round(time.time() * 1000))

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
                'company': self.company or 'None',
                'date': milliseconds,
                'plan': self.plan.name
            },
            'privateAttributeNames': ['account_type', 'state'],
        }

        return user

    def get_random_ld_user(self):
        user = {
            'key': str(uuid.uuid1()),
            'anonymous': True
        }
        return user


class AnonymousUser(AnonymousUserMixin):
    set_path = 'default'

    def __init__(self):
        super(AnonymousUserMixin, self).__init__()

    def get_ld_user(self):
        app_version = current_app.config['VERSION']
        user = {
            "key": str(uuid.uuid1()),
            "custom": {
                "app_version": app_version
            },
            "anonymous": True
        }

        return user


class Plan(db.Model):
    """
    Represents a plan type
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(120), index=True, unique=True)
    description = db.Column(db.String(250), index=True)
    cost = db.Column(db.Float())
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def get_plan_cost(self):
        return "{:,.2f}".format(self.cost)
