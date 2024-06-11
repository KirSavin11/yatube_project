from django.contrib.auth import get_user_model
from posts.forms import PostForm
from posts.models import Group, Post
from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.posts_count = Post.objects.count()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Enjoy',
            slug='test-slug'
        )
        cls.post = Post.objects.create(
            text='Тестовая запись',
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTests.user)

    def test_create_post(self):
        form_data = {
            'text': 'Тестовая запись',
            'author': self.user,
            'group': self.group
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        # self.assertRedirects(
        #    response, reverse(
        #       'posts:profile', kwargs={'username': self.user}
        #    )
        # )
        self.assertEqual(Post.objects.count(), self.posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовая запись',
                author=self.user,
                group=self.group,
            ).exists()
        )

    def test_edit_post(self):
        form_data = {
            'text': 'Изменённая запись поста',
            'author': self.user,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True,
        )
        self.assertEqual(
            Post.objects.filter(id=self.post.id).last().text,
            form_data['text']
        )
        self.assertRedirects(
            response, reverse(
                'posts:post_detail', kwargs={'post_id': self.post.id}
            )
        )
