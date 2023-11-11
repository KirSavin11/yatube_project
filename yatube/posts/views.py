from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    text = 'Это главная страница проекта Yatube'
    template = 'posts/index.html'
    context = {
        'text': text,
    }
    return render(request, template, context)


def group_posts(request, slug):
    text = 'Здесь будет информация о группах проекта Yatube'
    template = 'posts/group_list.html'
    context = {
        'text': text,
    }
    return render(request, template, context)
