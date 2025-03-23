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
    """Send a confirmation email to the user after paying for the subscription."""
    try:
        user = User.query.get(user_id)  # Fixed: Removed 'id = ' syntax error
        if not user:
            print(f"The user with id: {user_id} not found")
            raise ValueError(f"User with id {user_id} not found")

        msg = EmailMessage(
            subject="We sincerely hope your Emboldened experience provides functional utility",
            body=f"Hello {user.first_name} {user.last_name}, Thanks for your purchase and We hope that you enjoy your subscription. This is an automatic email, please don't reply to it",
            from_email=current_app.config['MAIL_USERNAME'],
            to=[user.email]
        )
        msg.send()
        print(f"Email sent to {user.email}")
        return True
    except Exception as e:
        raise ValueError(f"Email sending failed: {str(e)}") 
    
def send_email_licenses(user_id, licenses):
    """Send an email with the licenses available to the user."""
    try:
        user = User.query.get(user_id)
        if not user:
            error_msg = f"The user with id: {user_id} not found"
            print(error_msg)
            raise ValueError(error_msg)

        # Convert single string to list for consistent handling
        if isinstance(licenses, str):
            licenses = [licenses]
        elif not isinstance(licenses, (list, tuple)):
            raise ValueError("Licenses must be a string or a list of strings")

        # Create formatted license list
        license_text = "\n".join([f"License Key {i+1}: {license.license_key}" 
                                for i, license in enumerate(licenses)])
        
        body = (f"Hello Mr/Mrs {user.first_name} {user.last_name},\n\n"
                "Thank you for your subscription!\n"
                f"Here are your licenses:\n{license_text} \n"
                f"These licenses are valid for 365 days from {licenses[0].created_at} to {licenses[0].expires_at}\n"
                "We are excited for you and hope that your Emoldened experience provides measurable utility.\n Please do not reply to this email.")

        msg = EmailMessage(
            subject="Thank you for your annual subscription to Emboldened!",
            body=body,
            from_email=current_app.config['MAIL_USERNAME'],
            to=[user.email]
        )
        msg.send()
        print(f"Email sent to {user.email}")
        return True
        
    except Exception as e:
        error_msg = f"Email sending failed: {str(e)}"
        print(error_msg)
        raise ValueError(error_msg)
    
def send_email_free_trial(user_id, licenses):
    """Send an email with the licenses available to the user."""
    try:
        user = User.query.get(user_id)
        if not user:
            error_msg = f"The user with id: {user_id} not found"
            print(error_msg)
            raise ValueError(error_msg)
        
        body = (f"Hello Mr/Mrs {user.first_name} {user.last_name},\n\n"
                f"This {licenses.license_key} is valid for 14 days from {licenses.created_at} to {licenses.expires_at} \n"
                "We are excited for you and hope that your Emoldened experience provides measurable utility.\n Please do not reply to this email")

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
        error_msg = f"Email sending failed: {str(e)}"
        print(error_msg)
        raise ValueError(error_msg)