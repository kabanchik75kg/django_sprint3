from django.shortcuts import render, get_object_or_404

from .models import Post, Category


def index(request):
    post_list = Post.active_post().order_by('-pub_date')[:5]

    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, post_id):

    post = get_object_or_404(
        Post.active_post(),
        pk=post_id
    )

    return render(request, 'blog/detail.html',
                  {'post': post})


def category_posts(request, post_category):

    category = get_object_or_404(
        Category.objects.values(
            'title', 'description'
        ),
        slug=post_category, is_published=True
    )

    post_list = Post.active_post().filter(
        category__slug=post_category,
    )

    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html',
                  context)
