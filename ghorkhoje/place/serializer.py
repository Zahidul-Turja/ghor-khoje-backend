from django.utils import timezone

from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.db import transaction

from place.models import Place, Facility, Category, Image, PlaceReview
from user.models import User, Review


class FacilitySerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Facility
        fields = ("id", "name", "description", "slug", "bill", "icon")

    def get_icon(self, instance):
        request = self.context.get("request")
        if instance.icon:
            icon_url = instance.icon.url if hasattr(instance.icon, "url") else None
            return request.build_absolute_uri(icon_url) if icon_url else None
        return None


class CategorySerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "icon", "description")

    def get_icon(self, instance):
        request = self.context.get("request")
        if instance.icon:
            return (
                request.build_absolute_uri(instance.icon.url)
                if hasattr(instance.icon, "url")
                else None
            )
        return None


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
            "communication",
            "cleanliness",
            "maintenance",
            "privacy",
            "financial_transparency",
            "attitude",
            "overall",
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


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image", "description"]


class OwnerSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
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
            "profession",
            "hosted_places",
            "rating",
            "communication_rating",
            "cleanliness_rating",
            "maintenance_rating",
            "privacy_rating",
            "financial_transparency_rating",
            "attitude_rating",
            "reviews",
            "profile_image",
        ]

    def get_rating(self, instance):
        return instance.get_average_rating()

    def get_communication_rating(self, instance):
        return instance.get_average_communication_rating()

    def get_cleanliness_rating(self, instance):
        return instance.get_average_cleanliness_rating()

    def get_maintenance_rating(self, instance):
        return instance.get_average_maintenance_rating()

    def get_privacy_rating(self, instance):
        return instance.get_average_privacy_rating()

    def get_financial_transparency_rating(self, instance):
        return instance.get_average_financial_transparency_rating()

    def get_attitude_rating(self, instance):
        return instance.get_average_attitude_rating()

    def get_hosted_places(self, instance):
        return Place.objects.filter(owner=instance).count()

    def get_reviews(self, instance):
        reviews = instance.received_reviews.all()
        return ReviewSerializer(reviews, many=True).data


class PlaceReviewCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceReview
        fields = "__all__"


class PlaceReviewSerializer(serializers.ModelSerializer):
    reviewer = ReviewerSerializer()

    class Meta:
        model = PlaceReview
        fields = "__all__"


class PlaceDetailsSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    total_per_month = serializers.SerializerMethodField()
    facilities = FacilitySerializer(many=True, required=False)
    category = CategorySerializer(read_only=True)
    images = ImageSerializer(many=True, required=False)
    reviews = serializers.SerializerMethodField()
    avg_ratings = serializers.SerializerMethodField()

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
            "is_available",
            "featured",
            "is_active",
            "reviews",
            "avg_ratings",
        ]

    def get_avg_ratings(self, instance):
        res = {
            "cleanliness": instance.get_average_cleanliness_rating(),
            "description_match": instance.get_avarage_description_match_rating(),
            "location_convenience": instance.get_average_location_convenience_rating(),
            "value_for_money": instance.get_average_value_for_money_rating(),
            "neighborhood": instance.get_average_neighborhood_rating(),
            "overall": instance.get_average_overall(),
        }
        return res

    def get_reviews(self, instance):
        reviews = instance.reviews.all()
        return PlaceReviewSerializer(reviews, many=True).data

    def get_total_per_month(self, instance):
        if instance.extra_bills is None:
            return float(instance.rent_per_month)
        return instance.rent_per_month + instance.extra_bills


class PlaceSerializer(serializers.ModelSerializer):
    facilities = serializers.CharField(
        required=False, write_only=True, allow_blank=True
    )
    images = ImageSerializer(many=True, required=False, write_only=True)
    # images = serializers.ListField(child=ImageSerializer(), required=False)

    class Meta:
        model = Place
        fields = [
            "id",
            "title",
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
            "featured",
        ]

    def create(self, validated_data):
        print("Validated data:", validated_data)
        images_data = validated_data.pop("images", [])
        # facilities_data = validated_data.pop("facilities", [])
        facilities_data = list(validated_data.pop("facilities", []).split(","))
        owner = self.context["request"].user
        place = Place.objects.create(owner=owner, **validated_data)

        while transaction.atomic():
            for facility in facilities_data:
                if facility == "":
                    continue
                facility_instance = Facility.objects.get(id=facility)
                place.facilities.add(facility_instance)

            for image_data in images_data:
                Image.objects.create(place=place, **image_data)

            return place


class PlaceUpdateSerializer(serializers.ModelSerializer):
    facilities = FacilitySerializer(many=True, required=False)

    class Meta:
        model = Place
        fields = [
            "title",
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
            "featured",
        ]
