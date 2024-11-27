from constants import Constant
from django.shortcuts import get_object_or_404, render

from .models import Category, Post


def index(request):
    return render(
        request,
        "blog/index.html",
        {
            "post_list":
            Post.published_posts.all()[:Constant.COUNT_POSTS_ON_PAGE]
        }
    )


def post_detail(request, post_id):
    return render(
        request,
        "blog/detail.html",
        {
            "post": get_object_or_404(Post.published_posts.all(), pk=post_id)
        }
    )


def category_posts(request, post_category):
    category = get_object_or_404(
        Category,
        slug=post_category,
        is_published=True,
    )
    posts = category.posts(manager='published_posts').all()

    return render(
        request,
        "blog/category.html",
        {
            "category": category, "post_list": posts
        }
    )
