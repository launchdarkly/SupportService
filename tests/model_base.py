import unittest
from app.factory import SubdomainDispatcher
from app.models import db

class ModelBase(unittest.TestCase):
    def setUp(self):
        self.app = SubdomainDispatcher('localhost','default')
        env = {
            'LD_CLIENT_KEY': '12345',
            'LD_FRONTEND_KEY': '12345'
        }
        self.app = self.app.create_app('testing', env, config_name='testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
