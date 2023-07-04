from django.db import models
from django.contrib.auth import get_user_model

from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

User = get_user_model()


LIMIT_OF_COMMENT: int = 200
SIGNS_OF_REVIEW: int = 500


class Title(models.Model):
    pass


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
