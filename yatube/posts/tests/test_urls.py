from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.models import Group, Post

User = get_user_model()


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Hubabuba',
            author=cls.user,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTest.user)

    def test_common_pages(self):
        common_pages_urls = {
            '/': HTTPStatus.OK,
            f'/groups/{self.group.slug}/': HTTPStatus.OK,
            f'/profile/{self.user}/': HTTPStatus.OK,
            f'/posts/{self.post.id}/': HTTPStatus.OK,
            '/unexisting_page/': HTTPStatus.NOT_FOUND,
        }
        for address, status_code in common_pages_urls.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, status_code)

    # Проверяем доступность страниц для авторизованного пользователя

    def test_authorized_only_pages(self):
        authorized_only_pages = {
            '/create/': HTTPStatus.OK,
            f'/posts/{self.post.id}/edit/': HTTPStatus.OK,
        }
        for address, code_status in authorized_only_pages.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, code_status)

    # Проверяем редиректы для неавторизованного пользователя

    def test_create_redirect_anonymous(self):
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, ('/auth/login/?next=/create/')
        )

    def test_edit_redirect_anonymous(self):
        response = self.guest_client.get(f'/posts/{self.post.id}/edit/',
                                         follow=True)
        self.assertRedirects(
            response, (f'/posts/{self.post.id}/')
        )

    # Тестируем вызываемые шаблоны

    def test_urls_uses_correct_template(self):
        template_url_names = {
            '/': 'posts/index.html',
            f'/groups/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user}/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html',
        }
        for address, template in template_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
