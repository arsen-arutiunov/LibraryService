from users.models import User, UserManager
from django.test import TestCase
from django.db.utils import IntegrityError


class UserModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "testuser@example.com"
        password = "password123"
        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser is successful."""
        email = "superuser@example.com"
        password = "password123"
        user = User.objects.create_superuser(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_without_email_raises_error(self):
        """Test that creating a user without email raises a ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password="password123")

    def test_create_user_with_duplicate_email(self):
        """Test that creating a user with a duplicate email raises IntegrityError."""
        email = "duplicateuser@example.com"
        password = "password123"

        # Create the first user
        User.objects.create_user(email=email, password=password)

        # Try creating another user with the same email
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email=email, password="newpassword123")

    def test_create_user_with_empty_email_raises_value_error(self):
        """Test that creating a user with an empty email raises a ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="password123")
