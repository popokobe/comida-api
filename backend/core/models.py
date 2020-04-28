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


def profile_image_file_path(instance, filename):
    """Generate file path for new profile image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/profile/', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra__fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('メールアドレスは必須です。')
        if not username:
            raise ValueError('ユーザ名は必須です。')
        user = self.model(email=self.normalize_email(email),
                          username=username.lower(),
                          **extra__fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that has email and username"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=30, unique=True)
    fullname = models.CharField(max_length=60, blank=True)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(
        upload_to=profile_image_file_path, default='avatar.png')
    """
        The symmetrical field option means that
        you don't necessarily have to follow the person who follows you.
    """
    followers = models.ManyToManyField('self',
                                       related_name='user_followers',
                                       blank=True,
                                       symmetrical=False
                                       )
    following = models.ManyToManyField('self',
                                       blank=True,
                                       symmetrical=False
                                       )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def number_of_followers(self):
        """Retrieve number of people who follows a person"""
        if self.followers.count():
            return self.followers.count()
        else:
            return 0

    def number_of_following(self):
        """Retrieve number of people a person is follwing"""
        if self.following.count():
            return self.following.count()
        else:
            return 0

    def __str__(self):
        return self.username


class Post(models.Model):
    """Post object"""
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_posts'
    )
    posted_on = models.DateTimeField(auto_now_add=True)
    note = models.TextField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='likers',
                                   blank=True,
                                   symmetrical=False)

    class Meta:
        ordering = ['-posted_on']

    def number_of_likes(self):
        if self.likes.count():
            return self.likes.count()
        else:
            return 0

    def __str__(self):
        return f'{self.user}\'s post'


class Restaurant(models.Model):
    """Restaurant object to be used for a post"""
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    post = models.ForeignKey('Post',
                             on_delete=models.CASCADE,
                             related_name='post_restaurant')
    category = models.ForeignKey('Category',
                                 on_delete=models.PROTECT,
                                 related_name='post_category')
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
    post = models.ForeignKey('Post',
                             on_delete=models.CASCADE,
                             related_name='post_comments')
    posted_on = models.DateTimeField(auto_now_add=True)
    comment_body = models.CharField(max_length=255)

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return f'{self.user}\'s comment'
