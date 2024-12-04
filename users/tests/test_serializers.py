from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


USER_CREATE_URL = reverse("users:create")
USER_MANAGE_URL = reverse("users:manage")


class UserSerializerTest(APITestCase):
    def setUp(self):
        """Create a user instance for the tests"""
        self.user_data = {
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password123",
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.user.set_password(self.user_data["password"])
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_user_with_valid_data(self):
        """Test that a user can be created with valid data"""
        data = {
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "newpassword123",
        }
        response = self.client.post(USER_CREATE_URL, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=data["email"])
        self.assertTrue(user.check_password(data["password"]))
        self.assertEqual(user.email, data["email"])

    def test_create_user_without_password(self):
        """
        Test that the serializer raises an error if no password is provided
        """
        data = {
            "email": "testuser2@example.com",
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post(USER_CREATE_URL, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self):
        """Test updating a user's data"""
        update_data = {
            "first_name": "Updated",
            "last_name": "User",
            "password": "newpassword123",
        }
        response = self.client.patch(
            USER_MANAGE_URL, update_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "User")

        self.assertTrue(self.user.check_password("newpassword123"))

    def test_update_user_without_password(self):
        """Test updating a user without providing a password"""
        update_data = {"first_name": "Updated", "last_name": "User"}
        response = self.client.patch(
            USER_MANAGE_URL, update_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "User")

        self.assertTrue(self.user.check_password(self.user_data["password"]))

    def test_create_user_with_invalid_email(self):
        """Test that an error is raised when an invalid email is provided"""
        invalid_email_data = {
            "email": "invalidemail.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password123",
        }
        response = self.client.post(
            USER_CREATE_URL, invalid_email_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_short_password(self):
        """Test that an error is raised when the password is too short"""
        short_password_data = {
            "email": "shortpassword@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "123",
        }
        response = self.client.post(
            USER_CREATE_URL, short_password_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
