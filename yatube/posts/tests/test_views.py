from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Bubblegum',
            slug='test-slug'
        )
        cls.post = Post.objects.create(
            text='Hubabuba',
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostPagesTests.user)

    def test_page_uses_correct_template(self):
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}):
            'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': 'auth'}):
            'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}):
            'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}):
            'posts/create_post.html'
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Тестирование корректности переданного в шаблон контекста

    def test_index_get_correct_context(self):
        response = self.authorized_client.get(reverse('posts:index'))

        # Взяли рандомный элемент и проверили, что содержание
        # совпадает с ожидаемым

        check_object = response.context['page_obj'][-1]
        post_text_0 = check_object.text
        post_author_0 = check_object.author
        self.assertEqual(post_text_0, check_object.text)
        self.assertEqual(str(post_author_0), 'auth')

    def test_group_list_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug'})
        )
        group_posts = response.context['page_obj']
        check_object = response.context['page_obj'][0]
        post_text = check_object.text
        post_author = check_object.author
        # Имя группы
        self.assertNotIn(self.group, group_posts)
        # Количество постов в группе
        self.assertEqual(len(response.context['page_obj']), 1)
        # Случайный пост на соответствие текста и автора
        self.assertEqual(post_text, check_object.text)
        self.assertEqual(post_author, self.post.author)

    def test_profile_get_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user})
        )
        author = self.user
        self.assertEqual(response.context['full_name'], author)

    def test_post_detail_get_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        post_object = response.context['post']
        self.assertEqual(post_object.text, self.post.text)

    def test_post_create_get_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_create')
        )
        form = response.context.get('form')
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for field_name, expected in form_fields.items():
            with self.subTest(field_name=field_name):
                form_field = form.fields.get(field_name)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_get_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        )
        form = response.context.get('form')
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for field_name, expected in form_fields.items():
            with self.subTest(field_name=field_name):
                form_field = form.fields.get(field_name)
                self.assertIsInstance(form_field, expected)
