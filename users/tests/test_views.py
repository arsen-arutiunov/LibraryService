from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse


class CreateUserViewTest(APITestCase):
    def setUp(self):
        """Set up the URL for the create user view."""
        self.url = reverse("users:create")

    def test_create_user_success(self):
        """Test that a user can be created successfully with valid data."""
        data = {
            "email": "testuser@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "Password123",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.first().email,
                         data["email"])

    def test_create_user_with_short_password(self):
        """
        Test that creating a user with
        a short password results in a validation error.
        """
        data = {
            "email": "testuser@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "short",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Password must be at least 8 characters long.",
            response.data["password"]
        )


class ManageUserViewTest(APITestCase):
    def setUp(self):
        """Set up the user and authentication token."""
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            first_name="John",
            last_name="Doe",
            password="Password123",
        )
        self.token = RefreshToken.for_user(self.user)
        self.url = reverse("users:manage")

    def test_get_user_profile(self):
        """Test that the user can retrieve their own profile."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Authorize {str(self.token.access_token)}"
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["first_name"], self.user.first_name)
        self.assertEqual(response.data["last_name"], self.user.last_name)

    def test_update_user_profile(self):
        """Test that the user can update their own profile."""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Authorize {str(self.token.access_token)}"
        )
        data = {"first_name": "Updated", "last_name": "User"}
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "User")

    def test_unauthorized_access(self):
        """Test that a non-authenticated user cannot access the profile."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserTests(APITestCase):
    def setUp(self):
        """Set up a user for all tests."""
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            first_name="John",
            last_name="Doe",
            password="Password123",
        )

    def test_create_user(self):
        """Test the user creation view."""
        url = reverse("users:create")
        data = {
            "email": "newuser@example.com",
            "first_name": "Jane",
            "last_name": "Doe",
            "password": "newpassword123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=data["email"])
        self.assertEqual(user.first_name, data["first_name"])

    def test_user_update(self):
        """Test the update of user details."""
        url = reverse("users:manage")
        self.client.force_authenticate(user=self.user)
        data = {
            "first_name": "UpdatedName",
            "last_name": "UpdatedSurname",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "UpdatedName")
        self.assertEqual(self.user.last_name, "UpdatedSurname")
