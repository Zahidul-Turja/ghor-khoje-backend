from django.utils import timezone
from django.db.models import Q
from rest_framework import serializers

from ghorkhoje.settings import OTP_LENGTH
from user.models import *
from utils.responses import custom_exception


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    password = serializers.CharField()
    confirm_password = serializers.CharField()
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
        if data.get("password") != data.get("confirm_password"):
            custom_exception("Passwords do not match.")
        if data.get("password") == data.get("email"):
            custom_exception("Password cannot be same as email.")
        if data.get("password") == data.get("phone"):
            custom_exception("Password cannot be same as phone number.")

        return data


class RegisterUserOTPVerificationSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length=255)
    otp = serializers.CharField(required=True, max_length=OTP_LENGTH)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=255)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=255)
    new_password = serializers.CharField(required=True, max_length=255)
    confirm_password = serializers.CharField(required=True, max_length=255)

    def validate(self, data):
        user = self.context["request"].user
        if not user.check_password(data.get("old_password")):
            raise serializers.ValidationError("Invalid credentials.")
        if data.get("new_password") != data.get("confirm_password"):
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        if data.get("new_password") == data.get("old_password"):
            raise serializers.ValidationError(
                "New password cannot be same as old password."
            )
        return data

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class EmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length=255)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length=255)
    otp = serializers.CharField(required=True, max_length=OTP_LENGTH)
    new_password = serializers.CharField(required=True, max_length=255)
    confirm_password = serializers.CharField(required=True, max_length=255)

    def validate(self, data):
        if data.get("new_password") != data.get("confirm_password"):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def save(self, **kwargs):
        email = self.validated_data["email"]
        otp = self.validated_data["otp"]
        new_password = self.validated_data["new_password"]
        user = User.objects.filter(email=email).first()

        if user is None or user.otp != otp:
            raise serializers.ValidationError("Invalid credentials.")

        user.set_password(new_password)
        user.otp = None
        user.save()

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone",
            "full_name",
            "nid",
            "date_of_birth",
            "profile_image",
        ]


class LandlordApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandlordApplication
        fields = ["user", "application_date", "status"]
