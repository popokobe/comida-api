# from tempfile
# from os

# from PIL import Image

# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.urls import reverse

# from rest_framework import status
# from rest_framework.test import APIClient

# from core.models import Restaurant

# from post.serializers import RestaurantSerializer


# RESTAURANTS_URL = reverse('post:restaurant-list')


# def image_upload_url(restaurant_id):
#     """Return URL for restaurant image upload"""
#     return reverse('post:restaurant-upload-image', args=[restaurant_id])


# class RestaurantImageUploadTests(TestCase):
#     """Test uploading images to restaurant"""

#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             'test@example.com',
#             'secret'
#         )
#         self.client.force_authenticate(self.user)
