from django.http import JsonResponse
from rest_framework import generics, permissions

from .models import Payment
from .serializers import PaymentSerializer


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)


class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


def success_view(request):
    return JsonResponse({"message": "Payment successful!"})


def cancel_view(request):
    return JsonResponse({"message": "Payment was paused or canceled."})
