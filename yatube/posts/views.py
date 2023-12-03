from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required

from .models import Post, Group


def index(request):
    text = 'Последние обновления на сайте'
    template = 'posts/index.html'
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'text': text,
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def group_posts(request, slug):
    text = 'Записи сообщества'
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # posts = group.posts.all()[:10]
    context = {
        'text': text,
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)
