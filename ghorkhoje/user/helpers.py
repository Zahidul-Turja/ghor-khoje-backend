import random
from django.db.models import Q
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from ghorkhoje.settings import OTP_LENGTH
from user.models import User, Notification

from user.serializers import UserProfileSerializer
from utils.responses import custom_exception
from utils.services import send_custom_email


def send_otp_email(recipient_email, otp):
    subject = "Ghor Khojee - Verify OTP Code"
    from_email = settings.EMAIL_HOST_USER
    to = [recipient_email]

    text_content = f"Your OTP is: {otp}"  # fallback for non-HTML clients

    html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f9f9f9;">
            <div style="max-width: 500px; margin: auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <h2 style="text-align: center; color: #333333;">Verify Your Email</h2>
            <p style="font-size: 16px; color: #555;">Use the OTP below to verify your email address:</p>
            <div style="display: flex; justify-content: center; align-items: center; gap: 10px; margin: 20px 0;">
                {''.join([f'<div style="width: 40px; height: 50px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; background-color: #eef2f7; border: 1px solid #ccc; border-radius: 5px;">{digit}</div>' for digit in otp])}
            </div>
            <p style="font-size: 14px; color: #999;">This OTP is valid for 10 minutes. Please do not share it with anyone.</p>
            </div>
        </body>
        </html>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def generate_otp():
    # return "1234"
    return "".join(random.choices("0123456789", k=OTP_LENGTH))


def user_registration_service(payload):
    otp = generate_otp()
    payload["otp"] = otp
    payload.pop("confirm_password", None)

    user = User.objects.create_user(**payload)

    Notification.objects.create(
        user=user,
        title="Account Created",
        message="Your account has been created successfully.",
        type="success",
        is_read=False,
    )

    # send_custom_email(
    #     "Ghor Khojee OTP Verification",
    #     f"Your One Time Password (OTP) is: {otp}",
    #     [user.email],
    # )

    send_otp_email(user.email, otp)
    print(f"Generated OTP: {otp}")
    return user


def resend_otp_service(payload):
    email = payload.get("email")
    user = User.objects.filter(email=email).first()

    if user is None:
        custom_exception("User does not exist.")

    otp = generate_otp()
    user.otp = otp
    user.save()

    # send_custom_email(
    #     "Ghor Khojee OTP Verification",
    #     f"Your One Time Password (OTP) is: {otp}",
    #     [user.email],
    # )

    send_otp_email(user.email, otp)
    print(f"Resent OTP: {otp}")
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

    Notification.objects.create(
        user=user,
        title="Welcome to Ghor Khojee",
        message="Your account has been verified successfully.",
        type="success",
        is_read=False,
    )

    return True


def user_login_service(payload, request):
    email = payload.get("email")
    password = payload.get("password")

    try:
        user = User.objects.get(email=email)
        if user.is_active is False:
            custom_exception("User is not active. Please verify your email first.")
    except User.DoesNotExist:
        custom_exception("User does not exist.")

    if not user.check_password(password):
        custom_exception("Invalid credentials.")

    token = RefreshToken.for_user(user)
    update_last_login(None, user)

    serializer = UserProfileSerializer(user, context={"request": request})
    user = serializer.data

    return {
        "user": user,
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
