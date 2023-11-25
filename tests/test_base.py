from flask import current_app, url_for
from flask_testing import TestCase
from urllib.parse import urlparse

from app import create_app


class MainTest(TestCase):
    def create_app(self):
        return create_app({
            'TESTING': True,
            'WTF_CSRF_ENABLED': False
        })

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_index_redirects(self):
        response = self.client.get(url_for('index'))
        parsed_location = urlparse(response.location)
        self.assertEqual(parsed_location.path, url_for('hello'))

    def test_hello_get(self):
        response = self.client.get(url_for("hello"))
        self.assert200(response)

    def test_hello_post(self):
        fake_form = {
            'password': 'fake',
            'username': 'fake1'
        }

        response = self.client.post(url_for('hello'), data=fake_form)
        parsed_location = urlparse(response.location)
        self.assertEqual(parsed_location.path, url_for('hello'))

    def test_auth_blueprint_exist(self):
        self.assertIn('auth', self.create_app().blueprints)

    def test_auth_login_get(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)

    def test_auth_login_templete(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')
