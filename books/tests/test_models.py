from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from books.models import Book


class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=10,
            daily_fee=Decimal("2.50")
        )

    def test_book_creation(self):
        """Test that a book is created successfully with valid data"""
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.cover, Book.CoverType.HARD)
        self.assertEqual(self.book.inventory, 10)
        self.assertEqual(self.book.daily_fee, Decimal("2.50"))

    def test_str_representation(self):
        """Test the string representation of a book"""
        self.assertEqual(str(self.book), "Test Book (Test Author)")

    def test_inventory_validator(self):
        """Test that inventory must be greater than or equal to 1"""
        with self.assertRaises(ValidationError):
            book = Book(
                title="Invalid Inventory",
                author="Author",
                cover=Book.CoverType.SOFT,
                inventory=0,
                daily_fee=Decimal("1.00")
            )
            book.full_clean()

    def test_daily_fee_validator(self):
        """Test that daily fee must be greater than or equal to 0.01"""
        with self.assertRaises(ValidationError):
            book = Book(
                title="Invalid Fee",
                author="Author",
                cover=Book.CoverType.SOFT,
                inventory=5,
                daily_fee=Decimal("0.00")
            )
            book.full_clean()

    def test_cover_choices(self):
        """Test that only valid cover choices are allowed"""
        with self.assertRaises(ValidationError):
            book = Book(
                title="Invalid Cover",
                author="Author",
                cover="INVALID",
                inventory=5,
                daily_fee=Decimal("1.00")
            )
            book.full_clean()
