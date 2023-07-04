from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    )

    role = models.CharField(
        max_length=9,
        choices=USER_TYPE_CHOICES,
        default='U')

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
        return self.role == 'U'

    @property
    def is_moderator(self):
        return self.role == 'M'

    @property
    def is_admin(self):
        return self.role == 'A'
