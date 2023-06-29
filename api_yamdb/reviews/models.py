from django.db import models


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        # blank=False,
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        blank=False,
        unique=True
    )


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        blank=False,
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        blank=False,
        unique=True
    )


class Rating(models.Model):
    pass


class User(models.Model):
    pass


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        blank=False,
        max_length=256,
    )
    year = models.DateField(
        verbose_name='Год выпуска',
        blank=False,
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE,
        blank=False,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        blank=False,
        null=True,
    )
    rating = models.ForeignKey(
        Rating,
        verbose_name='Рейтинг',
        on_delete=models.CASCADE,
    )
