"""payment.py — Stripe payment integration for subscriptions."""
import os
import time
from typing import Optional
from pathlib import Path
import json

import stripe
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

# Price IDs — create these in Stripe Dashboard
# For now we use price_data for easy setup
PLANS = {
    "pro": {
        "name": "Pro",
        "price_vnd": 299000,
        "price_usd": 13,
        "features": [
            "Unlimited text generation",
            "All content types",
            "Video scripts + TTS",
            "All AI models",
            "API access",
        ],
    },
    "business": {
        "name": "Business",
        "price_vnd": 599000,
        "price_usd": 26,
        "features": [
            "Everything in Pro",
            "AI video generation",
            "Bulk generation",
            "Team members (up to 5)",
            "White-label option",
        ],
    },
}

# Subscription tracking
SUBSCRIPTIONS_FILE = Path("output/subscriptions.json")


def _load_subs() -> dict:
    if SUBSCRIPTIONS_FILE.exists():
        return json.loads(SUBSCRIPTIONS_FILE.read_text())
    return {}


def _save_subs(subs: dict):
    SUBSCRIPTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SUBSCRIPTIONS_FILE.write_text(json.dumps(subs, indent=2))


def create_checkout_session(plan: str, customer_email: str, success_url: str, cancel_url: str) -> dict:
    """Create a Stripe Checkout Session for subscription."""
    if not stripe.api_key:
        return {"error": "Stripe not configured", "available": False}

    plan_info = PLANS.get(plan)
    if not plan_info:
        return {"error": f"Unknown plan: {plan}"}

    try:
        # Create or get customer
        customers = stripe.Customer.list(email=customer_email, limit=1)
        if customers.data:
            customer = customers.data[0]
        else:
            customer = stripe.Customer.create(email=customer_email)

        # Create checkout session
        session = stripe.checkout.Session.create(
            customer=customer.id,
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"AI Content Generator — {plan_info['name']}",
                        "description": " • ".join(plan_info["features"][:3]),
                    },
                    "unit_amount": plan_info["price_usd"] * 100,  # cents
                    "recurring": {"interval": "month"},
                },
                "quantity": 1,
            }],
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                "plan": plan,
                "email": customer_email,
            },
        )

        return {
            "success": True,
            "checkout_url": session.url,
            "session_id": session.id,
        }
    except stripe.error.StripeError as e:
        return {"error": str(e), "available": True}


def create_one_time_payment(amount_usd: int, customer_email: str, success_url: str, cancel_url: str) -> dict:
    """Create a one-time payment session (for pay-as-you-go credits)."""
    if not stripe.api_key:
        return {"error": "Stripe not configured", "available": False}

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"AI Content Generator — {amount_usd}$ Credits",
                    },
                    "unit_amount": amount_usd * 100,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={"email": customer_email, "type": "credits"},
        )
        return {"success": True, "checkout_url": session.url}
    except stripe.error.StripeError as e:
        return {"error": str(e)}


def handle_webhook(payload: bytes, sig_header: str) -> dict:
    """Handle Stripe webhook events."""
    if not STRIPE_WEBHOOK_SECRET:
        return {"error": "Webhook secret not configured"}

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        return {"error": str(e)}

    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        # Payment successful
        metadata = data.get("metadata", {})
        email = metadata.get("email", "")
        plan = metadata.get("plan", "")
        if email and plan:
            _record_subscription(email, plan, data.get("customer"), data.get("subscription"))

    elif event_type == "customer.subscription.deleted":
        # Subscription cancelled
        customer_id = data.get("customer")
        if customer_id:
            _cancel_subscription(customer_id)

    return {"success": True, "type": event_type}


def _record_subscription(email: str, plan: str, customer_id: str, subscription_id: str):
    subs = _load_subs()
    subs[email] = {
        "plan": plan,
        "stripe_customer_id": customer_id,
        "stripe_subscription_id": subscription_id,
        "status": "active",
        "started_at": time.time(),
    }
    _save_subs(subs)
    # Also update user plan in auth
    from auth import upgrade_user_plan
    upgrade_user_plan(email, plan, customer_id)


def _cancel_subscription(customer_id: str):
    subs = _load_subs()
    for email, sub in subs.items():
        if sub.get("stripe_customer_id") == customer_id:
            sub["status"] = "cancelled"
            from auth import upgrade_user_plan
            upgrade_user_plan(email, "free")
    _save_subs(subs)


def get_subscription(email: str) -> Optional[dict]:
    subs = _load_subs()
    return subs.get(email)


def is_stripe_configured() -> bool:
    return bool(stripe.api_key)
