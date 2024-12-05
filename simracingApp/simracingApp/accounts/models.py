from django.contrib.auth.models import AbstractUser
from django.db import models

from simracingApp.accounts.choices import USER_ROLES


class User(AbstractUser):
    role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default='regular'
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.username
