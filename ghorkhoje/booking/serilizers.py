from rest_framework import serializers

from booking.models import Booking
from user.serializers import UserProfileSerializer
from place.serializer import PlaceListSerializer, PlaceListOwnerSerializer
from place.models import Place
from user.models import User


class BookingCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "place",
            "booked_by",
            "full_name",
            "email",
            "phone_number",
            "move_in_date",
            "move_out_date",
            "number_of_occupants",
            "note",
            "rent_per_month",
            "extra_bills",
            "num_prepayment_months",
            "latitude",
            "longitude",
            "area_in_sqft",
        ]


class BookingRequestListSerializer(serializers.ModelSerializer):
    place = serializers.SerializerMethodField()
    booked_by = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            "id",
            "place",
            "booked_by",
            "full_name",
            "email",
            "phone_number",
            "move_in_date",
            "move_out_date",
            "number_of_occupants",
            "note",
            "rent_per_month",
            "extra_bills",
            "num_prepayment_months",
            "latitude",
            "longitude",
            "area_in_sqft",
            "status",
        ]

    def get_place(self, obj):
        return (
            PlaceListOwnerSerializer(obj.place, context=self.context).data
            if obj.place
            else None
        )

    def get_booked_by(self, obj):
        user = User.objects.filter(id=obj.booked_by.id).first()
        if user:
            return UserProfileSerializer(user, context=self.context).data
        return None


class UpdateBookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["status"]
