from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category
import datetime


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.select_related('category').filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.datetime.now()
    ).order_by('-pub_date')[0:5]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.filter(
            is_published=True, category__is_published=True,
            pub_date__lte=datetime.datetime.now()
        ),
        pk=pk
    )

    template = 'blog/detail.html'
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(
            slug=category_slug, is_published=True
        )
    )

    post_list = Post.objects.select_related('category').filter(
        is_published=True,
        category__slug=category_slug,
        pub_date__lte=datetime.datetime.now()
    ).order_by('-pub_date')

    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)
