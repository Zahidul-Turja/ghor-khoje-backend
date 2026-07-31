from django.db.models.signals import pre_save
from django.dispatch import receiver

from user.models import LandlordApplication
from user.helpers import send_application_status_update_email


@receiver(pre_save, sender=LandlordApplication)
def notify_on_application_status_update(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        prev = LandlordApplication.objects.get(pk=instance.pk)
    except LandlordApplication.DoesNotExist:
        return

    if prev.status != instance.status:
        # Only send AFTER save succeeds
        def send_email():
            send_application_status_update_email(
                recipient_email=instance.user.email,
                status=instance.status,
                reason=instance.rejection_reason,
            )

        from django.db import transaction

        transaction.on_commit(send_email)
