from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.db.models import Avg

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment
)


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
        fields = ('id', 'title', 'score', 'text', 'author', 'pub_date')

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
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='text'
    )
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    description = serializers.CharField(required=False)
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating'
        )

    def create(self, validated_data):

        genres = validated_data.pop('genre')

        title = Title.objects.create(**validated_data)

        for genre in genres:
            title.genre.add(genre)

        return title

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['category'] = CategorySerializer(instance.category).data
        genres = Genre.objects.filter(slug__in=data['genre'])
        genre_data = GenreSerializer(genres, many=True).data
        data['genre'] = genre_data

        return data

    def get_rating(self, obj):

        rating = Review.objects.filter(
            title=obj.id
        ).aggregate(Avg("score"))['score__avg']

        return rating


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='text'
    )
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review')
