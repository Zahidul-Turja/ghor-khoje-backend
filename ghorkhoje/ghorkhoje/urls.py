from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from ghorkhoje.views import get_random_quote
from user.urls import auth_urlpatterns, user_urlpatterns, application_urlpatterns
from place.urls import place_urlpatterns
from booking.urls import booking_urlpatterns
from feedback.urls import feedback_urlpatterns

api_v1_urls = [
    path("auth/", include(auth_urlpatterns), name="auth_urls"),
    path("user/", include(user_urlpatterns), name="user_urls"),
    path("application/", include(application_urlpatterns), name="application_urls"),
    path("places/", include(place_urlpatterns), name="place_urls"),
    path("bookings/", include(booking_urlpatterns), name="booking_urls"),
    path("feedback/", include(feedback_urlpatterns), name="feedback_urls"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_v1_urls), name="api_v1"),
    path("health/", get_random_quote, name="get_random_quotes"),
]


if settings.ENVIRONMENT != "production":
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
