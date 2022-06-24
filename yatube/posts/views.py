"""Functions to to return the response."""
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def p_paginator(queryset, request):
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'paginator': paginator,
        'page_number': page_number,
        'page_obj': page_obj,
    }


def index(request):
    """Function sorts the data and sends it to the template."""
    title = "Последние обновления на сайте"
    post_list = Post.objects.all().order_by('-pub_date')
    context = {
        'title': title,
    }
    context.update(p_paginator(post_list, request))
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Function sorts the data and sends it to the template."""
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    context = {
        'group': group,
    }
    context.update(p_paginator(post_list, request))
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author).order_by("-pub_date").all()
    context = {
        'author': author,
    }
    context.update(p_paginator(post_list, request))
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {
        'post_id': post_id,
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST or None)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('posts:profile', username=request.user)
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id=post_id)
        return render(
            request,
            'posts/create_post.html',
            {'form': form, 'is_edit': True, 'post': post}
        )
    form = PostForm(instance=post)
    context = {
        'form': form,
        'is_edit': True,
        'post': post
        }
    return render(request, 'posts/create_post.html', context)
