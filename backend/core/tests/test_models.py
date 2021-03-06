from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(username='testuser', email='test@example.com',
                password='secret'):
    """Create a sample user"""
    return get_user_model().objects.create_user(username, email, password)


class ModelTests(TestCase):

    def test_create_user_with_username_and_email_successful(self):
        """Test creating a new user with an email is successful"""
        username = 'testuser'
        email = 'test@example.com'
        password = 'secret'
        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@EXAMPLE.COM'
        user = get_user_model().objects.create_user(email, 'secret')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'secret')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'testuser',
            'test@example.com',
            'secret'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_post_str(self):
        """Test the post string representation"""
        post = models.Post.objects.create(
            user=sample_user(),
            note='Test note'
        )

        self.assertEqual(str(post), f'{post.user.username}\'s post')

    @patch('uuid.uuid4')
    def test_restaurant_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.restaurant_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/restaurant/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
