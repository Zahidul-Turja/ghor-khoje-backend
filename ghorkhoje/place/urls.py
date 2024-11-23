from django.urls import path
from place.views import PlaceAPIView, CategoryAPIView, FacilityAPIView


place_urlpatterns = [
    path("", PlaceAPIView.as_view(), name="place"),
    path("categories/", CategoryAPIView.as_view(), name="category"),
    path("facilities/", FacilityAPIView.as_view(), name="facility"),
]
