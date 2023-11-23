from django.db import models
from django.contrib.auth import get_user_model
# from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.text

    class Meta:
        # verbose_name = _('Post')
        # verbose_name_plural = _('All posts')
        ordering = ['-pub_date']
