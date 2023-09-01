from unittest import TestCase

from pyreydenx import Client
from pyreydenx.exceptions import InvalidCredentialsError


class TestClient(TestCase):
    def test_client_empty_email(self):
        with self.assertRaises(ValueError) as ctx:
            Client('', '')
        self.assertTrue(str(ctx.exception).lower() == 'email is required')

    def test_client_empty_password(self):
        with self.assertRaises(ValueError) as ctx:
            Client('email', '')
        self.assertTrue(str(ctx.exception).lower() == 'password is required')

    def test_invalid_creds(self):
        with self.assertRaises(InvalidCredentialsError) as ctx:
            Client('email', 'password')
        self.assertIsInstance(ctx.exception, InvalidCredentialsError)
