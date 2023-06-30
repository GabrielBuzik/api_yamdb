from django.shortcuts import render
from django.shortcuts import get_object_or_404
from api.serializers import CommentSerializer, ReviewSerializer

from reviews.models import Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

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
            return ('any'(),)
        return ('moder'(),) # I dont' know what you want(create/destroy/update)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        review_id = int(self.kwargs.get('review_id'))
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        return self.get_review.comments.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ('any'(),)
        return ('moder'(),)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user, review=self.get_review)
