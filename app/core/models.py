import uuid
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin

from django.conf import settings


def restaurant_image_file_path(instance, filename):
    """Generate file path for new restaurant image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/restaurant/', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra__fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('メールアドレスは必須です。')
        user = self.model(email=self.normalize_email(email), **extra__fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Post(models.Model):
    """Post object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    note = models.TextField()

    def __str__(self):
        return self.title


class Restaurant(models.Model):
    """Restaurant object to be used for a post"""
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    image = models.ImageField(null=True, upload_to=restaurant_image_file_path)
    name = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    dish = models.CharField(max_length=255, blank=True)
    expense = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.name


class Category(models.Model):
    """Category object to be used for restaurants"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Comment(models.Model):
    """Comment object to be used for a post"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment_body = models.CharField(max_length=255)

    def __str__(self):
        return self.comment_body
