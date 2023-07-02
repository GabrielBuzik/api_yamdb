from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import (
    TitleViewSet, CategoryViewSet, GenreViewSet,
)


app_name = 'api'


router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
