from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

# from core.models import Post

# from post.serializers import PostSerializer

POSTS_URL = reverse('post:post-list')


class PublicPostApiTests(TestCase):
    """Test that publicly available post API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving posts"""
        res = self.client.get(POSTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePostApiTests(TestCase):
    """Test the authorized user posts API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'secret'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_a_new_post(self):
        """Test creating a new post"""
        payload = {
            'title': 'Test Post',
            'note': 'This restaurant is awesome.'
        }
        res = self.client.post(POSTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
