from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, permissions, status

from books.models import Book
from books.serializers import BookSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all books.",
        description="List all books.",
        responses={status.HTTP_200_OK: BookSerializer()},
    ),
    retrieve=extend_schema(
        summary="Retrieve a books by ID.",
        description="Retrieve a books by ID.",
        responses={status.HTTP_200_OK: BookSerializer()},
    ),
    create=extend_schema(
        summary="Create a new books.",
        description="Create a new books.",
        responses={status.HTTP_201_CREATED: BookSerializer()},
    ),
    update=extend_schema(
        summary="Update a books by ID.",
        description="Update a books by ID.",
        responses={status.HTTP_200_OK: BookSerializer()},
    ),
    partial_update=extend_schema(
        summary="Partially update a books by ID.",
        description="Partially update a books by ID.",
        responses={status.HTTP_200_OK: BookSerializer()},
    ),
    destroy=extend_schema(
        summary="Delete a books by ID.",
        description="Delete a books by ID.",
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
