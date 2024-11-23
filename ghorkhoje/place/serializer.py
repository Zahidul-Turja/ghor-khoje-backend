from rest_framework import serializers

from place.models import Place, Facility, Category, Image


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ("id", "name", "bill")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class PlaceSerializer(serializers.ModelSerializer):
    facilities = serializers.PrimaryKeyRelatedField(
        queryset=Facility.objects.all(), many=True, required=False
    )
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Place
        fields = [
            "id",
            "title",
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
            "extra_bills",
            "latitude",
            "longitude",
            "available_from",
            "is_active",
            "images",
        ]

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])
        facilities_data = validated_data.pop("facilities", [])

        place = Place.objects.create(**validated_data)
        for image_data in images_data:
            Image.objects.create(place=place, image=image_data)
        for facility_data in facilities_data:
            place.facilities.add(facility_data)

        return place
