from django.urls import path

from booking.views import BookingAPIView

booking_urlpatterns = [
    path("create/", BookingAPIView.as_view(), name="create_booking"),
]
