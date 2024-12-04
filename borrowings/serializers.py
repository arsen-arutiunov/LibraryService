from rest_framework import serializers
from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("expected_return_date", "book", "user")

    def validate(self, attrs):
        book = attrs.get("book")
        if book.inventory <= 0:
            raise serializers.ValidationError(
                "This book is not available for borrowing."
            )
        return attrs


class ReturnBorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("user", "book")
