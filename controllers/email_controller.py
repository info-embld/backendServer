# controllers/email_controller.py
from flask_mail import Message, Mail
from flask import current_app
from models.users import User

def send_update_email(subject, message, mail):
    """Send an email update to all users subscribed to the newsletter."""
    try:
        subbed_users = User.query.filter_by(newsletter_sub=True).all()
        if not subbed_users:
            print("No users subscribed to the newsletter.")
            return None

        for user in subbed_users:
            msg = Message(
                subject=subject,
                recipients=[user.email],
                body=message,
                sender=current_app.config['MAIL_USERNAME']
            )
            mail.send(msg)
            print(f"Email sent to {user.email}")
        return True
    except Exception as e:
        print(f"Failed to send emails: {e}")
        raise ValueError(f"Email sending failed: {str(e)}")
    

def send_email_confirmation(mail, user_id):
    """Send a confirmation email to the user after paying the subscription"""
    try: 
        user = User.query.get(id = user_id)
        if not user:
            print(f"the user with id: {user_id}")
        
        msg = Message(
            subject="Thanks for subscribing to our Software",
            recipients=user.email,
            body=f"Hello Mr/Mrs {user.first_name} {user.last_name}, Thanks for your purchase and We hope that you enjoy the subscription. This is an automatic email please don't reply to it",
            sender=current_app.config['MAIL_USERNAME']
        )
        mail.send(msg)
        print(f"Email sent to {user.email}")
        return True
    except Exception as e:
        raise ValueError(f"Email sending failed: {str(e)}")