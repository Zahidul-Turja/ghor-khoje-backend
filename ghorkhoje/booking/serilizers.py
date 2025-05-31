from rest_framework import serializers

from booking.models import Booking


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
