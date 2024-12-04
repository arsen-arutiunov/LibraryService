from django.test import TestCase
from books.models import Book

class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            inventory=10,
            daily_fee=2.5
        )

    def test_book_creation(self):
        """Test that a book can be created successfully"""
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.inventory, 10)
        self.assertEqual(self.book.daily_fee, 2.5)

    def test_str_representation(self):
        """Test the string representation of a book"""
        self.assertEqual(str(self.book), "Test Book (Test Author)")