from django.urls import path
from place.views import *


place_urlpatterns = [
    path("create/", PlaceAPIView.as_view(), name="place"),
    path("list/", PlaceListAPIView.as_view(), name="place_list"),
    path("categories/", CategoryAPIView.as_view(), name="category"),
    path("facilities/", FacilityAPIView.as_view(), name="facility"),
    path(
        "featured-properties/",
        FeaturedPlaceListAPIView.as_view(),
        name="featured_place_list",
    ),
    path("update/<str:slug>/", PlaceUpdateAPIView.as_view(), name="place_update"),
    path("delete/<str:slug>/", PlaceDeleteAPIView.as_view(), name="place_delete"),
    path("<str:slug>/", PlaceDetailsAPIView.as_view(), name="place_detail"),
    path(
        "toggle-bookmark/<str:slug>/",
        ToggleBookmarkPlaceAPIView.as_view(),
        name="bookmark_place",
    ),
    path("review/<str:slug>/", PlaceReviewAPIView.as_view(), name="place_review"),
    path(
        "review/update/<str:slug>/",
        PlaceReviewAPIView.as_view(),
        name="place_review_update",
    ),
]
