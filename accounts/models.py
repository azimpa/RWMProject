from django.contrib.auth.models import AbstractUser, Permission
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_user_permissions',
    )
