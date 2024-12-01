from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, permissions, status

from book.models import Book
from book.serializers import BookSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all books.",
        description="List all books.",
        responses={status.HTTP_200_OK: BookSerializer()},
    ),
    retrieve=extend_schema(
        summary="Retrieve a book by ID.",
        description="Retrieve a book by ID.",
        responses={status.HTTP_200_OK: BookSerializer()},
    ),
    create=extend_schema(
        summary="Create a new book.",
        description="Create a new book.",
        responses={status.HTTP_201_CREATED: BookSerializer()},
    ),
    update=extend_schema(
        summary="Update a book by ID.",
        description="Update a book by ID.",
        responses={status.HTTP_200_OK: BookSerializer()},
    ),
    partial_update=extend_schema(
        summary="Partially update a book by ID.",
        description="Partially update a book by ID.",
        responses={status.HTTP_200_OK: BookSerializer()},
    ),
    destroy=extend_schema(
        summary="Delete a book by ID.",
        description="Delete a book by ID.",
        responses={status.HTTP_204_NO_CONTENT: None},
    ),
)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
