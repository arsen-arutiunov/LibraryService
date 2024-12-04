from decimal import Decimal
from django.test import TestCase
from books.models import Book
from books.serializers import BookSerializer


class BookSerializerTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=10,
            daily_fee=Decimal("2.50")
        )
        self.serializer = BookSerializer(instance=self.book)

    def test_serializer_fields(self):
        """Test that the serializer contains the expected fields"""
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            {"id", "title", "author", "cover", "inventory", "daily_fee"}
        )

    def test_serializer_content(self):
        """Test that the serializer outputs the correct data"""
        data = self.serializer.data
        self.assertEqual(data["id"], self.book.id)
        self.assertEqual(data["title"], self.book.title)
        self.assertEqual(data["author"], self.book.author)
        self.assertEqual(data["cover"], self.book.cover)
        self.assertEqual(data["inventory"], self.book.inventory)
        self.assertEqual(Decimal(data["daily_fee"]), self.book.daily_fee)

    def test_valid_data(self):
        """Test serializer validation for valid data"""
        valid_data = {
            "title": "New Book",
            "author": "New Author",
            "cover": Book.CoverType.SOFT,
            "inventory": 5,
            "daily_fee": "1.50"
        }
        serializer = BookSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        book = serializer.save()
        self.assertEqual(book.title, valid_data["title"])
        self.assertEqual(book.author, valid_data["author"])
        self.assertEqual(book.cover, valid_data["cover"])
        self.assertEqual(book.inventory, valid_data["inventory"])
        self.assertEqual(book.daily_fee, Decimal(valid_data["daily_fee"]))

    def test_invalid_data_inventory(self):
        """Test serializer validation for invalid inventory"""
        invalid_data = {
            "title": "Invalid Book",
            "author": "Author",
            "cover": Book.CoverType.SOFT,
            "inventory": 0,
            "daily_fee": "1.00"
        }
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("inventory", serializer.errors)

    def test_invalid_data_daily_fee(self):
        """Test serializer validation for invalid daily_fee"""
        invalid_data = {
            "title": "Invalid Fee",
            "author": "Author",
            "cover": Book.CoverType.HARD,
            "inventory": 5,
            "daily_fee": "0.00"
        }
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("daily_fee", serializer.errors)

    def test_invalid_data_cover(self):
        """Test serializer validation for invalid cover type"""
        invalid_data = {
            "title": "Invalid Cover",
            "author": "Author",
            "cover": "INVALID",
            "inventory": 5,
            "daily_fee": "1.50"
        }
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("cover", serializer.errors)
