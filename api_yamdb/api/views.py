from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from reviews.models import Title, Category, Genre, Review, Title
from .serializers import (
    TitleSerializer, CategorySerializer, GenreSerializer,
    CommentSerializer, ReviewSerializer, TitleCreateAndUpdateSerializer
)
from api.serializers import CommentSerializer, ReviewSerializer
from users import permissions
from api.permissions import AuthorModeratorAdminOrReadOnly


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        Avg('reviews__score'))
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsGetOrAdmin, ]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug',)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateAndUpdateSerializer
        return TitleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        genre_slug = self.request.query_params.get('genre')
        category_slug = self.request.query_params.get('category')
        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorModeratorAdminOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'],
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'],
        )
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModeratorAdminOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsGetOrAdmin, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsGetOrAdmin, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
