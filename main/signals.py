
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import User
from main.utils import send_custom_email
import logging
from django.urls import reverse
from django.conf import settings
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def send_welcome_email_signal(sender, instance, created, **kwargs):
    if created:
        subject = "مرحبًا بك في منصة Trophy!"
        message_body = (
    "شكرًا لتسجيلك في منصة Trophy. نحن سعداء بانضمامك إلينا! "
    "اكتشف منصتنا وابدأ بالتسوق أو البيع بكل سهولة اليوم." )
        path = reverse(getattr(settings, "TROPHY_EMAIL_BUTTON_URL_NAME", "login"))
        # Build the full absolute URL
        button_url = f"{settings.SITE_DOMAIN}{path}"
        button_text = getattr(settings, "TROPHY_EMAIL_BUTTON_TEXT", "Click here")

        send_custom_email(
            user=instance,
            subject=subject,
            message_body=message_body,
            button_url=button_url,
            button_text=button_text,
        )
