from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from borrowings.models import Borrowing
from books.models import Book
from users.models import User
from rest_framework.test import APIClient


BORROWINGS_LIST_URL = reverse("borrowings:borrowing-list")


def get_borrowing_detail_url(borrowing_id):
    return reverse("borrowings:borrowing-detail", args=[borrowing_id])


class BorrowingViewSetTests(APITestCase):
    def setUp(self):
        """Create sample data for the tests."""
        self.user = User.objects.create_user(
            email="user@example.com",
            first_name="Test",
            last_name="User",
            password="password123"
        )

        self.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            password="adminpassword123",
        )

        self.book = Book.objects.create(
            title="Test Book",
            author="Author",
            inventory=5,
            daily_fee=5.00
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_borrowings(self):
        """Test that the borrowings list is returned correctly for a user."""
        Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date="2024-12-10"
        )
        response = self.client.get(BORROWINGS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user"], self.user.id)

    def test_admin_list_borrowings_by_user_id(self):
        """Test that an admin can list borrowings by user ID."""
        Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date="2024-12-10"
        )
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(
            f"{BORROWINGS_LIST_URL}?user_id={str(self.user.id)}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_borrowing(self):
        """Test that a borrowing is created successfully."""
        data = {
            "expected_return_date": "2024-12-10",
            "book": self.book.id,
            "user": self.user.id
        }
        response = self.client.post(BORROWINGS_LIST_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"], self.user.id)
        self.assertEqual(response.data["book"], self.book.id)

    def test_create_borrowing_with_unavailable_book(self):
        """
        Test that a borrowing cannot be created if the book is unavailable.
        """
        self.book.inventory = 0
        self.book.save()
        data = {
            "expected_return_date": "2024-12-10",
            "book": self.book.id,
            "user": self.user.id
        }
        response = self.client.post(BORROWINGS_LIST_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_book_successfully(self):
        """Test that a user can return a book successfully."""
        borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date="2024-12-10"
        )
        response = self.client.post(
            f"{get_borrowing_detail_url(borrowing.id)}return/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        borrowing.refresh_from_db()
        self.assertIsNotNone(borrowing.actual_return_date)

    def test_return_book_already_returned(self):
        """
        Test that returning a book that has already been return a 400 error.
        """
        borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date="2024-12-10"
        )
        borrowing.actual_return_date = "2024-12-05"
        borrowing.save()
        response = self.client.post(
            f"{get_borrowing_detail_url(borrowing.id)}return/"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"],
                         "This borrowing has already been returned.")

    def test_is_active_filter(self):
        """Test that the 'is_active' query parameter works as expected."""
        Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date="2024-12-10"
        )
        Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date="2024-12-10",
            actual_return_date="2024-12-05"
        )
        response_active = self.client.get(
            f"{BORROWINGS_LIST_URL}?is_active=true"
        )
        response_returned = self.client.get(
            f"{BORROWINGS_LIST_URL}?is_active=false"
        )
        self.assertEqual(len(response_active.data), 1)
        self.assertEqual(len(response_returned.data), 1)
