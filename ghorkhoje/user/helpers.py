from django.db.models import Q
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
import random

from ghorkhoje.settings import OTP_LENGTH
from user.models import User
from utils.responses import custom_exception


def generate_otp():
    return "1234"
    # return "".join(random.choices("0123456789", k=OTP_LENGTH))


def user_registration_service(payload):
    otp = generate_otp()
    payload["otp"] = otp

    User.objects.create_user(**payload)
    return True


def otp_verification_service(payload):
    email = payload.get("email")
    otp = payload.get("otp")
    user = User.objects.filter(email=email).first()

    if user is None or user.otp != otp:
        return False

    user.is_active = True
    user.otp = ""
    user.save()

    return True


def user_login_service(payload):
    email = payload.get("email")
    password = payload.get("password")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        custom_exception("User does not exist.")

    if not user.check_password(password):
        custom_exception("Invalid credentials.")

    token = RefreshToken.for_user(user)
    update_last_login(None, user)

    return {
        "user_id": user.id,
        "access_token": str(token.access_token),
        "refresh_token": str(token),
    }


def forget_password_service(payload):
    email = payload.get("email")
    user = User.objects.filter(email=email).first()

    if user is None:
        custom_exception("User does not exist.")

    otp = generate_otp()
    user.otp = otp
    user.save()

    return True
