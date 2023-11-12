from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Group


def index(request):
    text = 'Последние обновления на сайте'
    template = 'posts/index.html'
    posts = Post.objects.all()[:10]
    context = {
        'text': text,
        'posts': posts,
    }
    return render(request, template, context)


def group_posts(request, slug):
    text = 'Записи сообщества'
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).all()[:10]
    context = {
        'text': text,
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)
