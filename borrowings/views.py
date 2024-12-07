from datetime import date

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter
)
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingCreateSerializer,
    ReturnBorrowingSerializer
)
from helpers.telegram import send_telegram_message
from payments.utils import create_stripe_payment_session


@extend_schema_view(
    list=extend_schema(
        summary="List all borrowings.",
        description="List all borrowings with optional "
                    "filtering by user_id and is_active.",
        parameters=[
            OpenApiParameter(
                name="user_id",
                description="Filter borrowings by user ID.",
                required=False,
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name="is_active",
                description=(
                        "Filter borrowings by active status. "
                        "`true` for active borrowings (not returned), "
                        "`false` for returned borrowings."
                ),
                required=False,
                type=OpenApiTypes.BOOL,
            ),
        ],
        responses={status.HTTP_200_OK: BorrowingSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve a borrowing by ID.",
        description="Retrieve a borrowing by ID.",
        responses={status.HTTP_200_OK: BorrowingSerializer()},
    ),
    create=extend_schema(
        summary="Create a new borrowing.",
        description="Create a new borrowing.",
        responses={status.HTTP_201_CREATED: BorrowingCreateSerializer},
    ),
    return_borrowing=extend_schema(
        summary="Return a book.",
        description="Return a book.",
        responses={status.HTTP_200_OK: ReturnBorrowingSerializer},
    ),
)
class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("book", "user").all()
    permission_classes = [IsAuthenticated]

    http_method_names = ["get", "post", "head", "options"]

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        elif self.action == "return_borrowing":
            return ReturnBorrowingSerializer
        return BorrowingSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if not user.is_staff:
            queryset = queryset.filter(user=user)

        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if user_id is not None and user.is_staff:
            queryset = queryset.filter(user__id=user_id)

        if is_active is not None:
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false":
                queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_staff:
            serializer.validated_data["user"] = user
        borrowing = serializer.save()

        create_stripe_payment_session(borrowing, self.request)

        message = (
            f"<b>New Borrowing</b>\n"
            f"User: {borrowing.user.email}\n"
            f"Book: {borrowing.book.title}\n"
            f"Date of borrowing: {borrowing.borrow_date}\n"
            f"Expected return date: {borrowing.expected_return_date}"
        )
        send_telegram_message(message)

    @action(detail=True, methods=["post"], url_path="return")
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        user = request.user

        if borrowing.user != user and not user.is_staff:
            return Response(
                {
                    "error": "You can only return books borrowed by yourself,"
                             " or an admin can return for any user."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if borrowing.actual_return_date:
            return Response(
                {"error": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.return_borrowing_with_fine(actual_return_date=date.today())

        message = (
            f"<b>Book Returned</b>\n"
            f"User: {borrowing.user.email}\n"
            f"Book: {borrowing.book.title}\n"
            f"Borrow date: {borrowing.borrow_date}\n"
            f"Return date: {borrowing.actual_return_date}"
        )
        send_telegram_message(message)

        return Response(
            {"detail": "Borrowing successfully returned."},
            status=status.HTTP_200_OK
        )
