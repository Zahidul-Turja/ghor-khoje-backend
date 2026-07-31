from django.db.models.signals import pre_save
from django.dispatch import receiver

from user.models import LandlordApplication
from user.helpers import send_application_status_update_email

# @receiver(pre_save, sender=LandlordApplication)
# def notify_on_application_status_update(sender, instance, **kwargs):
#     prev = LandlordApplication.objects.filter(id=instance.id).first()
#     if not prev:
#         return

#     if prev.status != instance.status:
#         send_application_status_update_email(
#             recipient_email=prev.user.email,
#             status=instance.status,
#             reason=instance.rejection_reason,
#         )
