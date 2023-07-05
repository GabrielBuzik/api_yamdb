from django.shortcuts import render
from django.shortcuts import get_object_or_404
from api.serializers import CommentSerializer, ReviewSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response

from reviews.models import Title, Category, Genre
from .serializers import (
    TitleSerializer, CategorySerializer, GenreSerializer,
)

from reviews.models import Review, Title
from rest_framework.permissions import AllowAny, IsAuthenticated
from users import permissions


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_title(self):
        title_id = int(self.kwargs.get('title_id'))
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title.reviews.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user, title=self.get_title)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return (AllowAny(),)
        return ('permission_admin/moder'(),) # I dont' know what you want(create/destroy/update)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        review_id = int(self.kwargs.get('review_id'))
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        return self.get_review.comments.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return (AllowAny(),)
        return ('permission_admin/moder'(),)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user, review=self.get_review)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsGetOrAdmin,]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsGetOrAdmin,]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
