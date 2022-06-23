"""Functions to to return the response."""
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Group, Post, User
from .forms import PostForm


def index(request):
    """Function sorts the data and sends it to the template."""
    title = "Последние обновления на сайте"
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Function sorts the data and sends it to the template."""
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = group.title
    description = group.description
    context = {
        'group': group,
        'page_obj': page_obj,
        'title': title,
        'description': description,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = User.objects.get(username=username)
    post_list = Post.objects.filter(author=author).order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'author': author,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    author_id = post.author_id
    posts_count = Post.objects.filter(author=author_id).count()
    author = User.objects.get(id=author_id)
    text = post.text
    title = text[:30]
    context = {
        'post_id': post_id,
        'title': title,
        'posts_count': posts_count,
        'post': post,
        'author': author,
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
        else:
            return render(request, 'posts/create_post.html', {'form': form})
    else:
        form = PostForm()
        return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('posts:post_detail', post_id=post_id)
            else:
                return render(
                    request,
                    'posts/create_post.html',
                    {'form': form, 'is_edit': True, 'post': post}
                )
        else:
            form = PostForm(instance=post)
            context = {
                'form': form,
                'is_edit': True,
                'post': post
            }
        return render(request, 'posts/create_post.html', context)
    else:
        return redirect('posts:post_detail', post_id=post_id)
