from django.urls import path
from .views import (
    PaymentListView,
    PaymentDetailView,
    success_view,
    cancel_view
)

urlpatterns = [
    path("", PaymentListView.as_view(), name="payment-list"),
    path("<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
    path("success/", success_view, name="payment-success"),
    path("cancel/", cancel_view, name="payment-cancel"),
]

app_name = "payments"
