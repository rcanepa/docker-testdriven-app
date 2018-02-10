from sqlalchemy.exc import IntegrityError
from project import db
from project.api.users import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = User(
            username='justatest',
            email='test@test.com'
        )
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        user = User(
            username='justatest',
            email='test@test.com'
        )
        db.session.add(user)
        db.session.commit()
        duplicate_user = User(
            username='justatest',
            email='test2@test.com'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        user = User(
            username='justatest',
            email='test@test.com'
        )
        db.session.add(user)
        db.session.commit()
        duplicate_user = User(
            username='justatest2',
            email='test@test.com'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user(username='justatest', email='test@test.com')
        self.assertTrue(isinstance(user.to_json(), dict))
