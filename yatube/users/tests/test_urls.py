from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class UsersURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(UsersURLTest.user)

    def test_common_pages(self):
        common_pages = {
            '/auth/login/': HTTPStatus.OK,
            '/auth/signup/': HTTPStatus.OK,
        }
        for address, code_status in common_pages.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, code_status)

    def test_authorized_only_pages(self):
        authorized_pages = {
            '/auth/logout/': HTTPStatus.OK,
            '/auth/password_change/': HTTPStatus.FOUND,
            '/auth/password_change/done/': HTTPStatus.FOUND,
            '/auth/password_reset/': HTTPStatus.OK,
            '/auth/password_reset/done/': HTTPStatus.OK,
            '/auth/reset/done/': HTTPStatus.OK,
        }
        for address, code_status in authorized_pages.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, code_status)
