from app.models import User, Plan
from app.db import db
from model_base import ModelBase


class UserModelTestCase(ModelBase):

    def test_ld_user_hash(self):
        p = Plan(id=1, name='free')
        db.session.add(p)
        db.session.commit()
        u = User(email = 'test@example.com', plan_id=1)
        db.session.add(u)
        db.session.commit()
        emailHash = u.get_email_hash()
        userEmailHash = u.get_ld_user()['key']

        self.assertEqual(userEmailHash, emailHash)
