from celery import shared_task
from datetime import date
from borrowings.models import Borrowing
from helpers.telegram import send_telegram_message

@shared_task
def check_overdue_borrowings():
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lt=date.today(),
        actual_return_date__isnull=True
    )
    if not overdue_borrowings.exists():
        send_telegram_message("No borrowings overdue today!")
        return

    for borrowing in overdue_borrowings:
        message = (
            f"<b>Overdue Borrowing</b>\n"
            f"User: {borrowing.user.email}\n"
            f"Book: {borrowing.book.title}\n"
            f"Expected return date: {borrowing.expected_return_date}\n"
        )
        send_telegram_message(message)