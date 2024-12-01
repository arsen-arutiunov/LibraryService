from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    class CoverType(models.TextChoices):
        HARD = "HARD", "Hardcover"
        SOFT = "SOFT", "Softcover"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=4, choices=CoverType.choices, default=CoverType.SOFT
    )
    inventory = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of this specific book available in the library."
    )
    daily_fee = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Daily fee for borrowing the book (in $USD)."
    )

    def __str__(self):
        return f"{self.title} ({self.author})"
