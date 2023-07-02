from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    path('titles/', views.titles, name='titles_list'),
    path('titles/<int:titles_id>/', views.title_detail, name='title_detail'),

    path('categories/', views.categories, name='categories_list'),
    path(
        'categories/<slug:slug>/',
        views.category_titles,
        name='category_detail'
    ),

    path('genres/', views.genres, name='genres_list'),
    path('genres/<slug:slug>/', views.genre_titles, name='genre_detail'),


    # path('profile/<str:username>/', views.profile, name='profile'),
    # path('create/', views.post_create, name='post_create'),
    # path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    # path('posts/<int:post_id>/comment/',
    #      views.add_comment, name='add_comment'),
    # path('follow/', views.follow_index, name='follow_index'),
    # path(
    #     'profile/<str:username>/follow/',
    #     views.profile_follow,
    #     name='profile_follow'
    # ),
    # path(
    #     'profile/<str:username>/unfollow/',
    #     views.profile_unfollow,
    #     name='profile_unfollow'
    # ),
]
