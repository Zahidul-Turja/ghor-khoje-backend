from rest_framework import serializers

from booking.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["place", "booked_by", "status"]
