import stripe
from datetime import datetime


def create_monthly_subscription_by_email(email: str, price_id: str) -> dict:
    """
    Creates a recurring monthly subscription for a user via the Stripe API using their email address.

    Args:
        email (str): The user's email address
        price_id (str): The Stripe price ID for the monthly subscription (e.g., 'price_xxx')
        api_key (str): Your Stripe secret API key

    Returns:
        dict: Subscription details or error message
    """
    try:
        # Set Stripe API key
        stripe.api_key = st.secrets["stripe_api_key"]

        # Search for existing customer by email
        customers = stripe.Customer.search(query=f"email:'{email}'")

        if customers.data:
            # Use the first matching customer
            customer = customers.data[0]
        else:
            # Create a new customer if none exists
            customer = stripe.Customer.create(email=email)

        # Create subscription
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{"price": price_id}],
            payment_behavior='default_incomplete',
            expand=['latest_invoice.payment_intent']
        )

        # Return relevant subscription details
        return {
            'status': 'success',
            'subscription_id': subscription.id,
            'customer_id': customer.id,
            'subscription_status': subscription.status,
            'client_secret': (subscription.latest_invoice.payment_intent.client_secret
                              if subscription.latest_invoice.payment_intent else None),
            'created': datetime.fromtimestamp(subscription.created).isoformat()
        }

    except stripe.error.CardError as e:
        return {
            'status': 'error',
            'message': f"Card error: {e.user_message}"
        }
    except stripe.error.InvalidRequestError as e:
        return {
            'status': 'error',
            'message': f"Invalid request: {e.user_message}"
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f"An error occurred: {str(e)}"
        }