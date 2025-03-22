import stripe
from models.licenses import License  # Import from models/licenses.py
from models.users import User  # Import from models/users.py
from models.db_conf import db  # Import db from main.py
import os

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def create_payment_session(user_id, license_id, amount):
    """Create a Stripe checkout session for purchasing a license."""
    try:
        # Verify user and license exist
        user = User.query.get(user_id)
        license = License.query.get(license_id)
        if not user or not license:
            raise ValueError("User or License not found")

        # Create a Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {  # Fixed: price_data, not price_date
                    'currency': 'usd',
                    'product_data': {
                        'name': f'License Key for {user.email}',
                    },
                    'unit_amount': amount,  # Amount in cents (e.g., 1000 = $10.00)
                },
                'quantity': 1,  # Added comma for clarity
            }],
            mode='payment',
            success_url=os.getenv('STRIPE_SUCCESS_URL', 'http://localhost:5000/payment/success'),
            cancel_url=os.getenv('STRIPE_CANCEL_URL', 'http://localhost:5000/payment/cancel'),
            metadata={
                'user_id': str(user_id),
                'license_id': str(license_id)
            }
        )

        return {
            'session_id': session.id,
            'url': session.url  # Redirect user to this URL to complete payment
        }
    except stripe.StripeError as e:
        raise ValueError(f"Stripe error: {str(e)}")
    except ValueError as e:
        raise e
    except Exception as e:
        raise ValueError(f"Failed to create payment session: {str(e)}")

def process_payment(session_id):
    """Process a completed payment and activate the license."""
    try:
        # Retrieve the session from Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        
        if session.payment_status == 'paid':
            # Extract metadata
            user_id = int(session.metadata['user_id'])
            license_id = int(session.metadata['license_id'])

            # Fetch and update the license
            license = License.query.get(license_id)
            if not license:
                raise ValueError("License not found")

            license.is_active = True
            user = User.query.get(int(user_id))
            user.subbed = True
            db.session.commit()
            return {
                'status': 'success',
                'user_id': user_id,
                'license_id': license_id,
                'amount': session.amount_total  # In cents
            }
        else:
            return {'status': 'unpaid'}
    except stripe.StripeError as e:
        db.session.rollback()
        raise ValueError(f"Stripe error: {str(e)}")
    except ValueError as e:
        db.session.rollback()
        raise e
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Payment processing failed: {str(e)}")

def check_payment_status(session_id):
    """Check the status of a payment session."""
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return {
            'session_id': session.id,
            'payment_status': session.payment_status,
            'amount_total': session.amount_total  # In cents
        }
    except stripe.StripeError as e:
        raise ValueError(f"Stripe error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to check payment status: {str(e)}")
