# from django.core.paginator import Paginator
# from django.shortcuts import render, get_object_or_404
# from django.shortcuts import redirect
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.cache import cache_page

# from .models import Title, Category, Genre, User


NUMB_OF_POSTS = 10


def titles(request, titles_list):
    pass


def title_detail(request, title_id):
    pass


def categories(request, categories_list):
    pass


def category_titles(request, slug):
    pass
    # category = get_object_or_404(Category, slug=slug)
    # Category_list = group.posts.select_related('group')
    # context = {
    #     'category': category,
    #     'page_obj': get_page_object(request, titles_list),
    # }
    # return render(request, 'titles/category_list.html', context)


def genres(request, genres_list):
    pass


def genre_titles(request, slug):
    pass
    # genre = get_object_or_404(Category, slug=slug)
    # Genre_list = group.posts.select_related('group')
    # context = {
    #     'genre': genre,
    #     'page_obj': get_page_object(request, titles_list),
    # }
    # return render(request, 'titles/genre_list.html', context)
