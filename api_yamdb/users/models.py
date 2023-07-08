from django.contrib.auth.models import AbstractUser
from django.db import models


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )

    role = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='user',
        blank=True)

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    confirmation_code = models.CharField(
        max_length=36,
        unique=True,
        null=True,
        blank=True
    )

    @property
    def is_user(self):

        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN
