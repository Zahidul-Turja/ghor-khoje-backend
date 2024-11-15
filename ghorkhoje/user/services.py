from django.db.models import Q
import random

from ghorkhoje.settings import OTP_LENGTH
from user.models import User


def generate_otp():
    return "".join(random.choices("0123456789", k=OTP_LENGTH))


def user_registration_service(payload):
    otp = generate_otp()
    payload["otp"] = otp

    User.objects.create_user(**payload)
    return True


def otp_verification_service(payload):
    email_or_phone = payload.get("email_or_phone")
    otp = payload.get("otp")
    user = User.objects.filter(
        Q(email=email_or_phone) | Q(phone=email_or_phone)
    ).first()

    if user is None or user.otp != otp:
        return False

    user.is_active = True
    user.otp = ""
    user.save()

    return True
