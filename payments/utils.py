import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY

def create_stripe_payment_intent(amount, currency="usd"):
    intent = stripe.PaymentIntent.create(
        amount=int(amount * 100),
        currency=currency,
    )
    return intent
