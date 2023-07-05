from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import (
    TitleViewSet, CategoryViewSet, GenreViewSet,
    ReviewViewSet, CommentViewSet
)


app_name = 'api'


router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('reviews', ReviewViewSet, basename='reviews')
router.register(
    r'reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/', include(router.urls)),
]
