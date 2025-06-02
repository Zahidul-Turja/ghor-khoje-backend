from django.urls import path

from booking.views import *

booking_urlpatterns = [
    path("create-booking/", BookingAPIView.as_view(), name="create_booking"),
    path(
        "booking-requests/",
        BookingRequestListAPIView.as_view(),
        name="booking_requests",
    ),
    path(
        "update-booking-status/<int:pk>/",
        UpdateBookingStatusAPIView.as_view(),
        name="update_booking_status",
    ),
]
