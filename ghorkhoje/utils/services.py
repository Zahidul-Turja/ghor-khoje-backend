from django.core.mail import send_mail
from django.conf import settings


def send_custom_email(subject, message, recipient_list, from_email=None):
    if from_email is None:
        from_email = settings.EMAIL_HOST_USER

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
