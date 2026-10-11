# peer_lending_backend/src/security/stripe_client.py

import stripe

STRIPE_API_KEY = "YOUR_STRIPE_SECRET_KEY"
stripe.api_key = STRIPE_API_KEY

def create_payment_intent(amount_cents: int, currency: str = "usd", customer_email: str = None):
    intent = stripe.PaymentIntent.create(
        amount=amount_cents,
        currency=currency,
        receipt_email=customer_email,
        automatic_payment_methods={"enabled": True}
    )
    return intent

def create_payout(amount_cents: int, destination_account: str, currency: str = "usd"):
    transfer = stripe.Transfer.create(
        amount=amount_cents,
        currency=currency,
        destination=destination_account
    )
    return transfer
