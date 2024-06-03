from django.contrib.auth import get_user_model
from django.test import TestCase
from posts.models import Group, Post

User = get_user_model()


class PostsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            text='Hubabuba',
            author=cls.user
        )
        cls.group = Group.objects.create(
            title='BubbleGum'
        )

    # Method 1

    def test_str_post(self):
        post = PostsModelTest.post
        text = 'Hubabuba'
        self.assertEqual(
            post.__str__(), text
        )

    def test_str_group(self):
        group = PostsModelTest.group
        title = 'BubbleGum'
        self.assertEqual(
            group.__str__(), title
        )

    # Method 2

    def test_str_method(self):
        post = PostsModelTest.post
        group = PostsModelTest.group
        field_str_post = {
            'text': 'Hubabuba',
        }
        field_str_group = {
            'title': 'BubbleGum',
        }
        for field, expected_value in field_str_post.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post.__str__(), expected_value
                )
        for field, expected_value in field_str_group.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group.__str__(), expected_value
                )
        field_verboses_post = {
            'text': 'Текст поста',
            'author': 'Автор',
            'pub_date': 'Дата публикации',
            'group': 'Группа'
        }
        for field, expected_value in field_verboses_post.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value
                )
        field_help_text_post = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу'
        }
        for field, expected_value in field_help_text_post.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value
                )
