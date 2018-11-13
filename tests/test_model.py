from app.models import User
from model_base import ModelBase

class UserModelTestCase(ModelBase):

    def test_ld_user_hash(self):
        u = User(email = 'test@example.com')
        emailHash = u.get_email_hash()
        userEmailHash = u.get_ld_user()['key']

        self.assertEqual(userEmailHash, emailHash)
