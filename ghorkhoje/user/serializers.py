from django.utils import timezone
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import serializers

from ghorkhoje.settings import OTP_LENGTH
from user.models import *
from utils.responses import custom_exception

from place.models import Place
from place.serializer import CategorySerializer, ImageSerializer


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


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(required=True)


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
    address = serializers.SerializerMethodField()
    social_links = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    # cover_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "profile_image",
            "cover_image",
            "bio",
            "gender",
            "date_of_birth",
            "nid",
            "user_type",
            "profession",
            "address",
            "languages",
            "preferred_language",
            "social_links",
            "created_at",
        ]

    def get_address(self, obj):
        return {
            "address": obj.address,
            "country": obj.country,
            "state": obj.state,
            "city": obj.city,
        }

    def get_social_links(self, obj):
        return {
            "facebook": obj.facebook,
            "twitter": obj.twitter,
            "instagram": obj.instagram,
            "linkedin": obj.linkedin,
            "youtube": obj.youtube,
            "telegram": obj.telegram,
        }

    def get_profile_image(self, obj):
        request = self.context.get("request")
        if obj.profile_image:
            return (
                request.build_absolute_uri(obj.profile_image.url)
                if hasattr(obj.profile_image, "url")
                else None
            )
        return None


class UpdataProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "full_name",
            "phone",
            "profile_image",
            "cover_image",
            "bio",
            "gender",
            "date_of_birth",
            "nid",
            "profession",
            "address",
            "country",
            "state",
            "city",
            "languages",
            "preferred_language",
            "facebook",
            "twitter",
            "instagram",
            "linkedin",
            "youtube",
            "telegram",
        ]


class LandlordApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandlordApplication
        fields = ["user", "application_date", "status"]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "title", "message", "type", "status", "created_at", "is_read"]


class UpdateNotificationReadStatusSerializer(serializers.Serializer):
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="List of notification IDs to mark as read",
    )

    def validate_notification_ids(self, value):
        """
        Validate that all notification IDs exist and belong to the current user
        """
        if not value:
            raise serializers.ValidationError(
                "At least one notification ID is required."
            )

        # Remove duplicates while preserving order
        unique_ids = list(dict.fromkeys(value))

        # Get the current user from context
        user = self.context["request"].user

        # Check if all notifications exist and belong to the user
        existing_notifications = Notification.objects.filter(
            id__in=unique_ids,
            user=user,  # Assuming your Notification model has a user field
        ).values_list("id", flat=True)

        existing_ids = set(existing_notifications)
        requested_ids = set(unique_ids)

        # Check for non-existent or unauthorized notifications
        invalid_ids = requested_ids - existing_ids
        if invalid_ids:
            raise serializers.ValidationError(
                f"Invalid notification IDs: {list(invalid_ids)}. "
                "These notifications either don't exist or don't belong to you."
            )

        return unique_ids

    def save(self):
        """
        Update the is_read status of notifications to True
        """
        notification_ids = self.validated_data["notification_ids"]
        user = self.context["request"].user

        try:
            with transaction.atomic():
                # Update notifications to mark them as read
                updated_count = Notification.objects.filter(
                    id__in=notification_ids,
                    user=user,
                    is_read=False,  # Only update unread notifications
                ).update(is_read=True)

                return {
                    "updated_count": updated_count,
                    "notification_ids": notification_ids,
                }
        except Exception as e:
            raise ValidationError(f"Failed to update notifications: {str(e)}")


class ReviewerSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "full_name", "profile_image"]

    def get_profile_image(self, obj):
        request = self.context.get("request")
        if obj.profile_image:
            return (
                request.build_absolute_uri(obj.profile_image.url)
                if hasattr(obj.profile_image, "url")
                else None
            )
        return None


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = ReviewerSerializer()

    class Meta:
        model = Review
        fields = "__all__"


class PlaceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = [
            "id",
            "created_at",
            "title",
            "slug",
            "description",
            "city",
            "area_name",
            "area_code",
            "block_name",
            "street_name",
            "house_name",
            "house_number",
            "apartment_number",
            "floor_number",
            "rent_per_month",
            "extra_bills",
            "latitude",
            "longitude",
            "area_in_sqft",
            "num_of_bedrooms",
            "num_of_bathrooms",
            "num_of_balconies",
            "num_of_kitchens",
            "num_of_living_rooms",
            "num_of_dining_rooms",
            "num_of_parking_spaces",
            "capacity",
            "appointment_status",
            "available_from",
            "featured",
            "is_available",
            "category",
            "image",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.images.exists():
            image = obj.images.first()
            return (
                request.build_absolute_uri(image.image.url)
                if hasattr(image.image, "url")
                else None
            )
        return None


class AboutHostSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    social_links = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    average_rating = serializers.SerializerMethodField()
    communication_rating = serializers.SerializerMethodField()
    cleanliness_rating = serializers.SerializerMethodField()
    maintenance_rating = serializers.SerializerMethodField()
    privacy_rating = serializers.SerializerMethodField()
    financial_transparency_rating = serializers.SerializerMethodField()
    attitude_rating = serializers.SerializerMethodField()

    reviews = serializers.SerializerMethodField()
    hosted_places = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "profile_image",
            "bio",
            "gender",
            "date_of_birth",
            "user_type",
            "profession",
            "address",
            "languages",
            "preferred_language",
            "social_links",
            "created_at",
            "average_rating",
            "communication_rating",
            "cleanliness_rating",
            "maintenance_rating",
            "privacy_rating",
            "financial_transparency_rating",
            "attitude_rating",
            "reviews",
            "hosted_places",
        ]

    def get_address(self, obj):
        return {
            "address": obj.address,
            "country": obj.country,
            "state": obj.state,
            "city": obj.city,
        }

    def get_social_links(self, obj):
        return {
            "facebook": obj.facebook,
            "twitter": obj.twitter,
            "instagram": obj.instagram,
            "linkedin": obj.linkedin,
            "youtube": obj.youtube,
            "telegram": obj.telegram,
        }

    def get_profile_image(self, obj):
        request = self.context.get("request")
        if obj.profile_image:
            return (
                request.build_absolute_uri(obj.profile_image.url)
                if hasattr(obj.profile_image, "url")
                else None
            )
        return None

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_communication_rating(self, obj):
        return obj.get_average_communication_rating()

    def get_cleanliness_rating(self, obj):
        return obj.get_average_cleanliness_rating()

    def get_maintenance_rating(self, obj):
        return obj.get_average_maintenance_rating()

    def get_privacy_rating(self, obj):
        return obj.get_average_privacy_rating()

    def get_financial_transparency_rating(self, obj):
        return obj.get_average_financial_transparency_rating()

    def get_attitude_rating(self, obj):
        return obj.get_average_attitude_rating()

    def get_hosted_places(self, obj):
        return Place.objects.filter(owner=obj).count()

    def get_reviews(self, obj):
        reviews = obj.received_reviews.all()
        return ReviewSerializer(reviews, many=True, context=self.context).data

    def get_hosted_places(self, obj):
        places = obj.owned_places.all()
        return PlaceSerializer(places, many=True, context=self.context).data


# Task APIs
class TaskCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "user",
            "title",
            "description",
            "category",
            "priority",
            "due_date",
            "related_property",
        ]


class PlaceTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "title"]


class TaskSerializer(serializers.ModelSerializer):
    related_property = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "title",
            "description",
            "category",
            "priority",
            "due_date",
            "related_property",
            "is_complete",
            "created_at",
        ]

    def get_related_property(self, obj):
        return PlaceTitleSerializer(obj.related_property, context=self.context).data


class BookmarksSerializer(serializers.Serializer):
    place = serializers.SerializerMethodField()

    def get_place(self, obj):
        return PlaceTitleSerializer(obj.bookmarks, context=self.context, many=True).data
