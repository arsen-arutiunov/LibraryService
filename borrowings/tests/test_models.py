from datetime import date, timedelta
from django.test import TestCase
from books.models import Book
from users.models import User
from borrowings.models import Borrowing


class BorrowingModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            password="testpassword123"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Author Name",
            cover="SOFT",
            inventory=5,
            daily_fee=1.99
        )
        self.expected_return_date = date.today() + timedelta(days=7)

    def test_borrowing_creation(self):
        """
        Test that a Borrowing is created with the correct
        book, user, and dates.
        """
        borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            expected_return_date=self.expected_return_date
        )
        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(borrowing.user, self.user)
        self.assertEqual(borrowing.borrow_date, date.today())
        self.assertEqual(borrowing.expected_return_date,
                         self.expected_return_date)
        self.assertIsNone(borrowing.actual_return_date)

    def test_book_inventory_decreases_on_borrowing(self):
        """
        Test that the book inventory decreases by 1
        when a Borrowing is created.
        """
        Borrowing.objects.create(
            book=self.book,
            user=self.user,
            expected_return_date=self.expected_return_date
        )
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 4)

    def test_return_book(self):
        """
        Test that 'return_book' updates
        the inventory and sets the return date.
        """
        borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            expected_return_date=self.expected_return_date
        )
        borrowing.return_book()
        self.book.refresh_from_db()
        borrowing.refresh_from_db()
        self.assertEqual(self.book.inventory, 5)
        self.assertEqual(borrowing.actual_return_date, date.today())

    def test_is_active(self):
        """
        Test that 'is_active' reflects the correct status
        based on the return date.
        """
        borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            expected_return_date=self.expected_return_date
        )
        self.assertTrue(borrowing.is_active())
        borrowing.return_book()
        self.assertFalse(borrowing.is_active())

    def test_str_representation(self):
        """Test the string representation: "<user> borrowed <book>"."""
        borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            expected_return_date=self.expected_return_date
        )
        self.assertEqual(str(borrowing), f"{self.user} borrowed {self.book}")
