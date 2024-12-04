from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from borrowings.models import Borrowing
from books.models import Book
from users.models import User
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingCreateSerializer,
    ReturnBorrowingSerializer,
)


class BorrowingSerializerTests(APITestCase):

    def setUp(self):
        """Create sample data for the tests."""
        self.user = User.objects.create_user(
            email="user@example.com",
            first_name="Test",
            last_name="User",
            password="password123",
        )
        self.book = Book.objects.create(
            title="Test Book", author="Author", inventory=5, daily_fee=5.00
        )
        self.borrowing = Borrowing.objects.create(
            user=self.user, book=self.book, expected_return_date="2024-12-10"
        )

    def test_borrowing_serializer(self):
        """Test that the BorrowingSerializer returns the correct data."""
        serializer = BorrowingSerializer(self.borrowing)
        data = serializer.data
        self.assertEqual(data["user"], self.user.id)
        self.assertEqual(data["book"], self.book.id)
        self.assertEqual(
            data["expected_return_date"],
            str(self.borrowing.expected_return_date)
        )


class BorrowingCreateSerializerTests(APITestCase):

    def setUp(self):
        """Create sample data for the tests."""
        self.user = User.objects.create_user(
            email="user@example.com",
            first_name="Test",
            last_name="User",
            password="password123",
        )
        self.book = Book.objects.create(
            title="Test Book", author="Author", inventory=5, daily_fee=5.00
        )

    def test_valid_borrowing_create(self):
        """Test that BorrowingCreateSerializer creates a valid borrowing."""
        data = {
            "expected_return_date": "2024-12-10",
            "book": self.book.id,
            "user": self.user.id,
        }
        serializer = BorrowingCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        borrowing = serializer.save()
        self.assertEqual(borrowing.user, self.user)
        self.assertEqual(borrowing.book, self.book)

    def test_borrowing_create_with_unavailable_book(self):
        """
        Test that BorrowingCreateSerializer raises a validation error
        when the book is not available.
        """
        self.book.inventory = 0
        self.book.save()
        data = {
            "expected_return_date": "2024-12-10",
            "book": self.book.id,
            "user": self.user.id,
        }
        serializer = BorrowingCreateSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class ReturnBorrowingSerializerTests(APITestCase):
    def setUp(self):
        """
        Create data for the tests.
        """
        self.user = User.objects.create_user(
            email="user@example.com",
            first_name="Test",
            last_name="User",
            password="password123",
        )
        self.book = Book.objects.create(
            title="Test Book", author="Author", inventory=5, daily_fee=5.00
        )
        self.borrowing = Borrowing.objects.create(
            user=self.user, book=self.book, expected_return_date="2024-12-10"
        )

    def test_return_borrowing_serializer(self):
        """
        Test that the ReturnBorrowingSerializer
        correctly handles returning a book.
        """
        data = {"user": self.user.id, "book": self.book.id}
        serializer = ReturnBorrowingSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["user"], self.user)
        self.assertEqual(serializer.validated_data["book"], self.book)
