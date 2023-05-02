"""
Database models
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.postgres.fields import ArrayField


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password, **extra_fields):
        """Create, save and return a new user"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        if not email:
            raise ValueError('User must have an email address.')
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Electrocardiogram(models.Model):
    """Electrocardiogram object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'


class Lead(models.Model):
    """Electrocardiogram object."""
    electrocardiogram = models.ForeignKey(
        Electrocardiogram,
        related_name='leads',
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    samples = models.IntegerField()
    signal = ArrayField(models.IntegerField())

    def __str__(self):
        return f'name:{self.name} signal:{self.signal}'
