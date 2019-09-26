import unittest

from flask import current_app

from app.factory import create_app
from app.db import db


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        #self.app = SubdomainDispatcher('localhost','default')
        env = {
            'LD_CLIENT_KEY': '12345',
            'LD_FRONTEND_KEY': '12345'
        }
        self.app = create_app('testing', env, config_name='testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_app_exists(self):
        self.assertFalse(current_app is None)


    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
