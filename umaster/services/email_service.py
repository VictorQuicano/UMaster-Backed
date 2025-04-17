from django.conf import settings
from django.urls import reverse
from umaster.utils import Util


class EmailService:
    """Service specialized in sending pre-formated emails"""

    # TODO: Add templates for emails, were are waiting for the frontend to be ready
    @staticmethod
    def send_verification_email(user, token):
        """Sends an email to verify the user with a token"""
        current_site = settings.FRONTEND_URL
        relative_link = reverse("email-verify")
        absolute_url = f"{current_site}{relative_link}?token={str(token)}"
        email_body = f"Hi {user.username}, use the link below to verify your email \n{absolute_url}"

        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Verify your email",
        }

        Util.send_email(data)

    @staticmethod
    def send_password_reset_email(user, token):
        """Sends an email to reset the password with a token"""
        current_site = settings.FRONTEND_URL
        relative_link = reverse("reset-password")
        absolute_url = f"{current_site}{relative_link}?token={str(token)}"
        email_body = f"Hi {user.username}, use the link below to reset your password \n{absolute_url}"

        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Reset your password",
        }

        Util.send_email(data)