from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id", "user", "borrowing", "amount", "status", "created_at")
        read_only_fields = ("id", "created_at", "user", "status")
