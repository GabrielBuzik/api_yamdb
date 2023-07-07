from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title



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


    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
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