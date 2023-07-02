from rest_framework import serializers
# from django.shortcuts import get_object_or_404

from reviews.models import Title, Category, Genre


class TitleSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

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
