from django.utils import timezone

from rest_framework import serializers
from django.core.exceptions import ValidationError

from place.models import Place, Facility, Category, Image
from user.models import User, Review


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ("id", "name", "bill")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image", "description"]


class ReviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "profile_image"]


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = ReviewerSerializer()
    review_date = serializers.SerializerMethodField()
    reviewed_days_ago = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "reviewer",
            "review_text",
            "rating",
            "review_date",
            "reviewed_days_ago",
        ]

    def get_review_date(self, instance):
        return instance.created_at.strftime("%Y-%m-%d") if instance.created_at else None

    def get_reviewed_days_ago(self, instance):
        if instance.created_at:
            days_ago = (timezone.now() - instance.created_at).days
            return f"{days_ago} days ago"
        return None


class OwnerSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    hosted_places = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "profession",
            "hosted_places",
            "rating",
            "reviews",
            "profile_image",
        ]

    def get_rating(self, instance):
        return instance.get_average_rating()

    def get_hosted_places(self, instance):
        return Place.objects.filter(owner=instance).count()

    def get_reviews(self, instance):
        reviews = instance.received_reviews.all()
        return ReviewSerializer(reviews, many=True).data


class PlaceSerializer(serializers.ModelSerializer):
    facilities = FacilitySerializer(many=True, required=False)
    images = ImageSerializer(many=True, required=False)
    total_per_month = serializers.SerializerMethodField()
    owner = OwnerSerializer()

    class Meta:
        model = Place
        fields = [
            "id",
            "title",
            "slug",
            "owner",
            "description",
            "category",
            "facilities",
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
            "total_per_month",
            "extra_bills",
            "num_prepayment_months",
            "latitude",
            "longitude",
            "available_from",
            "is_active",
            "images",
            "num_of_bedrooms",
            "num_of_bathrooms",
            "num_of_balconies",
            "num_of_kitchens",
            "num_of_living_rooms",
            "num_of_dining_rooms",
            "num_of_parking_spaces",
            "area_in_sqft",
            "capacity",
            "appointment_status",
            "created_at",
        ]

    def get_total_per_month(self, instance):
        return instance.rent_per_month + instance.extra_bills

    def create(self, validated_data):
        print("Validated Data: ", validated_data)
        images_data = validated_data.pop("images")
        facilities_data = validated_data.pop("facilities", [])
        place = Place.objects.create(**validated_data)

        # Add images if provided
        for image_data in images_data:
            Image.objects.create(place=place, **image_data)

        for facility_data in facilities_data:
            place.facilities.add(facility_data)

        return place
