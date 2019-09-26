import unittest
from app.factory import create_app
from app.db import db

class ModelBase(unittest.TestCase):
    def setUp(self):
        env_id = '12345'
        env_api_key = '12345'
        self.app = create_app(env_id, env_api_key, config_name='testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
