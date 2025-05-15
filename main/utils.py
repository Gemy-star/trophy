
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import datetime

def send_custom_email(user, subject, message_body, button_url=None, button_text=None):
    """
    Sends an HTML email using the custom template with the given parameters.
    """
    context = {
        "subject": subject,
        "user_name": user.get_full_name() or user.email,
        "message_body": message_body,
        "button_url": button_url,
        "button_text": button_text,
        "year": datetime.datetime.now().year,
    }

    html_content = render_to_string("email/notification.html", context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
