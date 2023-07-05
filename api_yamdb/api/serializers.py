from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Title, Category, Genre
from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Title.objects.all(),
        required=False
    )
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('score', 'text', 'author', 'pub_date')

    def validate(self, data):
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(
                author_id=user.id, title_id=title_id
            ).exists():
                raise serializers.ValidationError(
                    'Отзыв уже существует.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('review',)


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


# class PostSerializer(serializers.ModelSerializer):
#     # author = serializers.SlugRelatedField(
#     #     slug_field='username',
#     #     read_only=True
#     # )
#     # pub_date = serializers.DateTimeField(read_only=True)
#     # id = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Post
#         fields = ('__all__')

