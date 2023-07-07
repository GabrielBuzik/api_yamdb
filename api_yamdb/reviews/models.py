from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
from . validators import validate_year

LIMIT_OF_COMMENT: int = 200
SIGNS_OF_REVIEW: int = 500


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    year = models.IntegerField(
        validators=[validate_year],
        verbose_name='Год выпуска',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='Жанр',
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )
    rating = models.FloatField(null=True)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        db_index=True,
        null=False
    )
    text = models.TextField('Содержание отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
        db_index=True,
        null=False
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        null=False,
        validators=(
            MinValueValidator(1, 'Минимум 1',),
            MaxValueValidator(10, 'Максимум 10',)
        ),
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_title_author'
            ),
        )

    def __str__(self):
        return self.text[:SIGNS_OF_REVIEW]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Произведение',
        db_index=True,
        null=False
    )
    text = models.TextField(null=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
        db_index=True,
        null=False
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:LIMIT_OF_COMMENT]
