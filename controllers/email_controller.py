from flask_mailman import EmailMessage
from flask import current_app
from models.users import User

def send_update_email(subject, message):
    """Send an email update to all users subscribed to the newsletter."""
    try:
        subbed_users = User.query.filter_by(newsletter_sub=True).all()
        if not subbed_users:
            print("No users subscribed to the newsletter.")
            return None

        for user in subbed_users:
            msg = EmailMessage(
                subject=subject,
                body=message,
                from_email=current_app.config['MAIL_USERNAME'],
                to=[user.email]
            )
            msg.send()
            print(f"Email sent to {user.email}")
        return True
    except Exception as e:
        print(f"Failed to send emails: {e}")
        raise ValueError(f"Email sending failed: {str(e)}")

def send_email_confirmation(user_id):
    """Send a confirmation email to the user after paying the subscription."""
    try:
        user = User.query.get(user_id)  # Fixed: Removed 'id = ' syntax error
        if not user:
            print(f"The user with id: {user_id} not found")
            raise ValueError(f"User with id {user_id} not found")

        msg = EmailMessage(
            subject="Thanks for subscribing to our Software",
            body=f"Hello Mr/Mrs {user.first_name} {user.last_name}, Thanks for your purchase and We hope that you enjoy the subscription. This is an automatic email please don't reply to it",
            from_email=current_app.config['MAIL_USERNAME'],
            to=[user.email]
        )
        msg.send()
        print(f"Email sent to {user.email}")
        return True
    except Exception as e:
        raise ValueError(f"Email sending failed: {str(e)}")
    
def send_email_licenses(user_id, licenses):
    """Send an email with the licenses available to the user"""
    try:
        user = User.query.get(user_id)

        if not user:
            print(f"The user with id: {user_id} not found")
            raise ValueError(f"The user with id: {user_id} not found")
        
        if isinstance(licenses, str):
            licenses = [licenses]
        elif not isinstance(licenses, (list, tuple)):
            raise ValueError("Licenses must be a string or a list of strings")
        
        license_text = "\n".join([f"License Key {i+1}: {license}" 
                                for i, license in enumerate(licenses)])
        
        body = (f"Hello Mr/Mrs {user.first_name} {user.last_name},\n\n"
                f"Here are the licenses that you have now:\n{license_text}")

        msg = EmailMessage(
            subject="Licenses available right now",
            body=body,
            from_email=current_app.config['MAIL_USERNAME'],
            to=[user.email]
        )
        msg.send()
        print(f"Email sent to {user.email}")
        return True
    except Exception as e:
        raise ValueError(f"Email sending Failed: {str(e)}")