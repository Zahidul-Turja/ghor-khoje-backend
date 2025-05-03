from django.urls import path
from place.views import *


place_urlpatterns = [
    path("create/", PlaceAPIView.as_view(), name="place"),
    path("list/", PlaceListAPIView.as_view(), name="place_list"),
    path("categories/", CategoryAPIView.as_view(), name="category"),
    path("facilities/", FacilityAPIView.as_view(), name="facility"),
    path("<str:slug>/", PlaceDetailsAPIView.as_view(), name="place_detail"),
]
