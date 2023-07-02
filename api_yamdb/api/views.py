from rest_framework import viewsets
# from rest_framework import filters

from reviews.models import Title, Category, Genre
from .serializers import (
    TitleSerializer, CategorySerializer, GenreSerializer,
)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # search_fields = ('following__user', 'user__username')


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
