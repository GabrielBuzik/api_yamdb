from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import (
    TitleViewSet, CategoryViewSet, GenreViewSet, ReviewSerializer, CommentSerializer
)


app_name = 'api'


router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
# router.register('reviews', ReviewSerializer)
# router.register('comments', CommentSerializer, basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
]
