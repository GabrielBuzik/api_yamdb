from django.db import models
from django.contrib.auth import get_user_model

from django.core.validators import MaxValueValidator, MinValueValidator


User = get_user_model()


LIMIT_OF_COMMENT: int = 200
SIGNS_OF_REVIEW: int = 500


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


class Review(models.Model):
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
            MaxValueValidator(5, 'Максимум 5',)
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
                fields=('author',),
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

