from django.contrib.auth import get_user_model
from rest_framework import serializers

from books.models import Book
from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    payments = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        source="payment_set"
    )

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "payments",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.none(),
        required=False
    )

    class Meta:
        model = Borrowing
        fields = ("id", "expected_return_date", "book", "user")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        if user.is_staff:
            self.fields["user"].queryset = get_user_model().objects.all()
        else:
            self.fields["user"].queryset = get_user_model().objects.filter(
                id=user.id
            )

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.is_staff:
            attrs["user"] = user

        book = attrs.get("book")
        if book.inventory <= 0:
            raise serializers.ValidationError(
                "This book is not available for borrowing."
            )

        return attrs


class ReturnBorrowingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.none(),
        required=False
    )

    class Meta:
        model = Borrowing
        fields = ("book", "user")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user

        self.fields["book"].queryset = Book.objects.filter(
            id=Borrowing.objects.get(
                id=self.context["view"].kwargs["pk"]
            ).book.id
        )
        if user.is_staff:
            self.fields["user"].queryset = get_user_model().objects.all()
        else:
            self.fields["user"].queryset = get_user_model().objects.filter(
                id=user.id
            )

    def validate(self, attrs):
        borrowing = self.instance
        user = self.context["request"].user
        if borrowing.user != user and not user.is_staff:
            raise serializers.ValidationError(
                "You can only return books borrowed by yourself, "
                "or an admin can return for any user."
            )
        if borrowing.actual_return_date:
            raise serializers.ValidationError(
                "This borrowing has already been returned.")
        return attrs
