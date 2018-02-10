import json
from flask import current_app
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestAuthBlueprint(BaseTestCase):
    def test_user_registration(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'justatest',
                    'email': 'test@test.com',
                    'password': '123456'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_user_registration_duplicate_email(self):
        add_user(
            username='justatest',
            email='test@test.com',
            password='password'
        )
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'justatest2',
                    'email': 'test@test.com',
                    'password': 'password'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertEqual(
                data['message'],
                'Sorry. That user already exists.'
            )
            self.assert400(response)

    def test_user_registration_duplicate_username(self):
        add_user(
            username='justatest',
            email='test@test.com',
            password='password'
        )
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'justatest',
                    'email': 'test@test2.com',
                    'password': 'password'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertEqual(
                data['message'],
                'Sorry. That user already exists.'
            )
            self.assert400(response)

    def test_user_registration_invalid_json_keys_no_username(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'email': 'test@test2.com',
                    'password': 'password'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid payload.')
            self.assert400(response)

    def test_user_registration_invalid_json_keys_no_email(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'justatest',
                    'password': 'password'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid payload.')
            self.assert400(response)

    def test_user_registration_invalid_json_keys_no_password(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'justatest',
                    'email': 'test@test.com',
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid payload.')
            self.assert400(response)

    def test_registered_user_login(self):
        with self.client:
            add_user(
                username='justatest',
                email='test@test.com',
                password='password'
            )
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'password'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(isinstance(data['auth_token'], str))
            self.assertTrue(response.content_type == 'application/json')
            self.assert200(response)

    def test_not_registered_user_login(self):
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'password'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assert401(response)

    def test_valid_logout(self):
        add_user(
            username='justatest',
            email='test@test.com',
            password='password'
        )
        with self.client:
            # user login
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'password'
                }),
                content_type='application/json'
            )
            # valid logout token
            auth_token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {auth_token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assert200(response)

    def test_invalid_logout_expired_token(self):
        add_user(
            username='justatest',
            email='test@test.com',
            password='password'
        )
        with self.client:
            current_app.config['TOKEN_EXPIRATION_SECONDS'] = -1

            # user login
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'password'
                }),
                content_type='application/json'
            )

            auth_token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {auth_token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertEqual(
                data['message'],
                'Signature expired. Please log in again.'
            )
            self.assert401(response)

    def test_invalid_logout(self):
        with self.client:
            # invalid logout token
            auth_token = 'invalid-token'
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {auth_token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertEqual(
                data['message'],
                'Invalid token. Please log in again.'
            )
            self.assert401(response)

    def test_user_status(self):
        add_user(
            username='justatest',
            email='test@test.com',
            password='password'
        )
        with self.client:
            # user login
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'password'
                }),
                content_type='application/json'
            )

            auth_token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.get(
                '/auth/status',
                headers={'Authorization': f'Bearer {auth_token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['username'] == 'justatest')
            self.assertTrue(data['data']['email'] == 'test@test.com')
            self.assertTrue(data['data']['active'] is True)
            self.assert200(response)

    def test_invalid_user_status(self):
        with self.client:
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': 'Bearer invalid-token'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertEqual(
                data['message'],
                'Invalid token. Please log in again.'
            )
            self.assert401(response)
