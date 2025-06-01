from django.urls import path

from booking.views import BookingAPIView

booking_urlpatterns = [
    path("create-booking/", BookingAPIView.as_view(), name="create_booking"),
]
