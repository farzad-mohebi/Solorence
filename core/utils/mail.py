import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from notification.models import Notification


class MailService:

    def __init__(self, sender=None):
        self.sender = sender or settings.DEFAULT_FROM_EMAIL

    def render_and_send(self, subject, email, template, context, ):
        html_message = render_to_string(template, context)
        email_message = EmailMessage(
            subject,
            html_message,
            self.sender,  # From email
            [email],  # To email
        )
        email_message.content_subtype = 'html'
        email_message.mixed_subtype = 'related'
        if settings.EMAIL_ENABLED:
            email_message.send()
        else:
            print('EMAIL DISABLED:', email, subject, )

    def send_signup_link(self, email, signup_link, username=None, subject=None):
        subject = subject or "Signup to Solorence"
        context = {
            'username': username or email.split('@')[0],
            'signup_link': signup_link,
            'year': datetime.datetime.now().year,
        }
        try:
            self.render_and_send(
                subject=subject,
                email=email,
                template='mail/signup.html',
                context=context,
            )
        except Exception as e:
            print("Send Email Failed: ", e)
            return False
        return True

    def send_notification(self, notification: Notification):
        subject = notification.text
        user = notification.user
        context = {
            'subject': subject,
            'username': user.username
        }
        try:
            self.render_and_send(
                subject=subject,
                email=user.email,
                template='mail/notification.html',
                context=context,
            )
        except Exception as e:
            print("Send Email Failed: ", e)
            return False
        return True
