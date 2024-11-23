from django.urls import path
from place.views import PlaceAPIView


place_urlpatterns = [
    path("", PlaceAPIView.as_view(), name="place"),
]
