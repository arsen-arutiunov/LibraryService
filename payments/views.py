import stripe
from django.http import JsonResponse
from django.views import View
from rest_framework import generics, permissions, serializers

from LibraryService import settings

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView

from helpers.telegram import send_telegram_message
from .models import Payment
from .serializers import PaymentSerializer
from borrowings.models import Borrowing
from .utils import create_stripe_payment_session


stripe.api_key = settings.STRIPE_API_KEY


class PaymentListView(ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        borrow_id = self.request.data.get("borrowing")

        if not borrow_id:
            raise serializers.ValidationError(
                {"borrowing": "This field is required."})

        try:
            borrowing = Borrowing.objects.get(id=borrow_id)
        except Borrowing.DoesNotExist:
            raise serializers.ValidationError(
                {"borrowing": "Borrowing not found."})

        payment, session = create_stripe_payment_session(borrowing,
                                                         self.request)

        serializer.instance = payment


class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)


class PaymentSuccessView(View):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")  # Получаем session_id из URL
        if not session_id:
            return JsonResponse({"error": "Missing session_id"}, status=400)

        try:
            session = stripe.checkout.Session.retrieve(session_id)

            if session.payment_status == "paid":
                payment = Payment.objects.get(session_id=session_id)
                payment.status = "Success"
                payment.save()

                send_telegram_message(
                    f"Payment for Borrowing ID {payment.borrowing.id}"
                    f" has been successfully processed."
                )

                return JsonResponse({"status": "Payment successful"})
            else:
                return JsonResponse({"status": "Payment failed"})

        except stripe.error.StripeError as e:
            return JsonResponse({"error": str(e)}, status=500)


class PaymentCancelView(View):
    def get(self, request, *args, **kwargs):
        send_telegram_message("Payment was canceled. Please try again later.")
        return JsonResponse(
            {"message": "Payment was canceled. Please try again later."}
        )
