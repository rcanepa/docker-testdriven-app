from sqlalchemy.exc import IntegrityError
from project import db
from project.api.users import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = User(
            username='justatest',
            email='test@test.com',
            password='password'
        )
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.active)
        self.assertTrue(user.password)

    def test_add_user_duplicate_username(self):
        user = User(
            username='justatest',
            email='test@test.com',
            password='password'
        )
        db.session.add(user)
        db.session.commit()
        duplicate_user = User(
            username='justatest',
            email='test2@test.com',
            password='password'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        user = User(
            username='justatest',
            email='test@test.com',
            password='password'
        )
        db.session.add(user)
        db.session.commit()
        duplicate_user = User(
            username='justatest2',
            email='test@test.com',
            password='password'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user(
            username='justatest',
            email='test@test.com',
            password='password'
        )
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        user_one = add_user('justatest', 'test@test.com', 'test')
        user_two = add_user('justatest2', 'test@test2.com', 'test')
        self.assertNotEqual(user_one.password, user_two.password)

    def test_encode_auth_token(self):
        user = add_user(
            username='justatest',
            email='test@test.com',
            password='password'
        )
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(User.decode_auth_token(auth_token), user.id)
