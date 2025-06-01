import stripe
import streamlit as st
from datetime import datetime


def create_checkout_session_for_subscription(email: str, price_id: str) -> dict:
    """
    Creates a Stripe Checkout Session for a recurring monthly subscription using the user's email.

    Args:
        email (str): The user's email address
        price_id (str): The Stripe price ID for the monthly subscription (e.g., 'price_xxx')
        api_key (str): Your Stripe secret API key
        success_url (str): URL to redirect to after successful payment (e.g., 'https://your-site.com/success')
        cancel_url (str): URL to redirect to if the user cancels (e.g., 'https://your-site.com/cancel')

    Returns:
        dict: Checkout Session details or error message
    """
    try:
        # Set Stripe API key
        stripe.api_key = st.secrets["stripe_api_key"]

        # Search for existing customer by email
        customers = stripe.Customer.search(query=f"email:'{email}'")

        if customers.data:
            customer = customers.data[0]
        else:
            customer = stripe.Customer.create(email=email)

        # Create a Checkout Session
        session = stripe.checkout.Session.create(
            customer=customer.id,
            payment_method_types=['card', 'paypal'],
            success_url='https://steamers.streamlit.app/',
            cancel_url='https://steamers.streamlit.app/',
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',  # Set to subscription for recurring payments
            subscription_data={
                'description': 'Monthly subscription'
            }
        )

        # Return session details
        return {
            'status': 'success',
            'session_id': session.id,
            'session_url': session.url,
            'customer_id': customer.id,
            'created': datetime.fromtimestamp(session.created).isoformat()
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
