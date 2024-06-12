from django.contrib.auth import get_user_model
from django.db import models

# from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Выберите группу'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        # verbose_name = _('Post')
        # verbose_name_plural = _('All posts')
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Введите текст'
    )
    created = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        # verbose_name = _('Post')
        # verbose_name_plural = _('All posts')
        ordering = ('-created',)

    def __str__(self):
        return self.text[:15]
