from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework import filters
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

from reviews.models import Title, Category, Genre
from .serializers import (
    TitleSerializer, CategorySerializer, GenreSerializer,
    CommentSerializer, ReviewSerializer, TitleCreateAndUpdateSerializer
)

from api.serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review, Title
from rest_framework.permissions import AllowAny
from users import permissions


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
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
    permission_classes = [permissions.IsGetOrAdmin, ]

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review())

    def create(self, request, *args, **kwargs):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, id=review_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, review=review)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsGetOrAdmin, ]

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title)


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
