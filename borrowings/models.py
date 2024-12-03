from datetime import date

from django.db import models

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book,
                             on_delete=models.CASCADE,
                             related_name="borrowings")
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="borrowings")

    def save(self, *args, **kwargs):
        """Borrowing"""
        if not self.pk:
            self.book.inventory -= 1
            self.book.save()
        super().save(*args, **kwargs)

    def return_book(self):
        if not self.actual_return_date:
            self.actual_return_date = date.today()
            self.book.inventory += 1
            self.book.save()
            self.save()

    def is_active(self):
        return not self.actual_return_date

    is_active.boolean = True

    def __str__(self):
        return f"{self.user} borrowed {self.book}"
