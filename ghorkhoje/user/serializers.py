from rest_framework import serializers

from ghorkhoje.settings import OTP_LENGTH
from user.models import User
from utils.responses import custom_exception


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    password = serializers.CharField()
    full_name = serializers.CharField()
    nid = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    profile_image = serializers.ImageField(required=False)

    def validate(self, data):
        if not data.get("email") and not data.get("phone"):
            custom_exception("Please provide either email or phone number.")
        if User.objects.filter(email=data.get("email")).exists() and data.get("email"):
            custom_exception("User with this email already exists.")
        if User.objects.filter(phone=data.get("phone")).exists() and data.get("phone"):
            custom_exception("User with this phone number already exists.")
        if User.objects.filter(nid=data.get("nid")).exists() and data.get("nid"):
            custom_exception("User with this NID already exists.")

        return data


class RegisterUserOTPVerificationSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(required=True, max_length=255)
    otp = serializers.CharField(required=True, max_length=OTP_LENGTH)


class UserLoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=255)
