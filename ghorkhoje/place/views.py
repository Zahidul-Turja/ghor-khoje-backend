import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q
from django.utils.timezone import now, timedelta

from place.models import *
from place.serializer import *
from user.models import Notification
from utils.responses import common_response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class FacilityAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = FacilitySerializer

    def get(self, request):
        try:
            facilities = Facility.objects.all().order_by("name")
            serializer = FacilitySerializer(
                facilities, many=True, context={"request": request}
            )
            if request.accepted_renderer.format == "api":
                return Response(serializer.data)
            return common_response(
                200, "Facilities fetched successfully.", serializer.data
            )
        except Exception as e:
            return common_response(400, str(e))


class CategoryAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    def get(self, request):
        try:
            categories = Category.objects.all().order_by("name")
            serializer = CategorySerializer(
                categories, many=True, context={"request": request}
            )
            if request.accepted_renderer.format == "api":
                return Response(serializer.data)
            return common_response(
                200, "Categories fetched successfully.", serializer.data
            )
        except Exception as e:
            return common_response(400, str(e))


# class PlaceListAPIView(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = PlaceDetailsSerializer
#     pagination_class = StandardResultsSetPagination

#     def get(self, request):
#         try:
#             category_slug = request.query_params.get("category", "all")
#             search_query = request.query_params.get("search", "").strip().lower()
#             date_range = request.query_params.get(
#                 "date_range", None
#             )  # last 7 days / last 30 days / all time
#             sort_by_price = request.query_params.get("sort_by_price", "created_at")

#             category = Category.objects.filter(slug=category_slug).first()
#             places = (
#                 Place.objects.filter(category=category, is_available=True)
#                 if category_slug != "all"
#                 else Place.objects.filter(is_available=True).all()
#             )
#             paginator = self.pagination_class()
#             paginated_places = paginator.paginate_queryset(places, request)
#             serializer = self.serializer_class(
#                 paginated_places, many=True, context={"request": request}
#             )
#             return paginator.get_paginated_response(serializer.data)
#         except Exception as e:
#             return common_response(400, str(e))


class PlaceListAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PlaceDetailsSerializer
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        try:
            category_slug = request.query_params.get("category", "all")
            search_query = request.query_params.get("search", "").strip().lower()
            date_range = request.query_params.get(
                "date_range", None
            )  # 'last_7_days', 'last_30_days', 'all'
            sort_by_price = request.query_params.get(
                "sort_by_price", "created_at"
            )  # 'low_to_high' / 'high_to_low'

            # Get Category
            category = (
                Category.objects.filter(slug=category_slug).first()
                if category_slug != "all"
                else None
            )

            # Base queryset
            places = Place.objects.filter(is_available=True)
            if category:
                places = places.filter(category=category)

            # Filter: Search
            if search_query:
                places = places.filter(
                    Q(title__icontains=search_query)
                    | Q(description__icontains=search_query)
                )

            # Filter: Date Range
            if date_range == "last_7_days":
                places = places.filter(created_at__gte=now() - timedelta(days=7))
            elif date_range == "last_30_days":
                places = places.filter(created_at__gte=now() - timedelta(days=30))
            # else 'all' means no filter

            # Sorting
            if sort_by_price == "low_to_high":
                places = places.order_by("rent_per_month")
            elif sort_by_price == "high_to_low":
                places = places.order_by("-rent_per_month")
            else:
                places = places.order_by("-created_at")  # default

            # Pagination & Serialization
            paginator = self.pagination_class()
            paginated_places = paginator.paginate_queryset(places, request)
            serializer = self.serializer_class(
                paginated_places, many=True, context={"request": request}
            )
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            traceback.print_exc()
            return common_response(400, str(e))


class PlaceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            print(request.data, "-------------------------------------")
            # Normalize scalar fields (convert single-item lists to strings/numbers)
            normalized_data = {
                key: value[0] if isinstance(value, list) else value
                for key, value in request.data.lists()
                if not key.startswith("images[")
            }

            # Process nested images list
            images = []
            index = 0
            while f"images[{index}].image" in request.FILES:
                image = request.FILES[f"images[{index}].image"]
                description = request.data.get(f"images[{index}].description", "")
                images.append({"image": image, "description": description})
                index += 1

            normalized_data["images"] = images

            # Proceed with serializer
            serializer = PlaceSerializer(
                data=normalized_data, context={"request": request}
            )

            if serializer.is_valid(raise_exception=True):
                place = serializer.create(serializer.validated_data)

                Notification.objects.create(
                    user=request.user,
                    title="Place Created",
                    message="Place created successfully.",
                    type="success",
                    is_read=False,
                )

                return common_response(
                    201,
                    "Place created successfully.",
                    PlaceDetailsSerializer(place, context={"request": request}).data,
                )
            else:
                Notification.objects.create(
                    user=request.user,
                    title="Place Creation Failed",
                    message="Something went wrong. Please try again later or contact support.",
                    type="error",
                    is_read=False,
                )
                return common_response(400, "Invalid data.", serializer.errors)
        except Exception as e:
            traceback.print_exc()
            return common_response(400, str(e))


class PlaceUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, slug):
        try:
            place = Place.objects.filter(slug=slug).first()
            if not place:
                return common_response(404, "Place not found.")

            if place.owner != request.user:
                return common_response(
                    403, "You are not authorized to update this place."
                )

            serializer = PlaceUpdateSerializer(
                place, data=request.data, partial=True, context={"request": request}
            )
            if serializer.is_valid():
                place = serializer.save()
                return common_response(
                    200,
                    "Place updated successfully.",
                    PlaceDetailsSerializer(place, context={"request": request}).data,
                )
            else:
                return common_response(400, "Invalid data.", serializer.errors)
        except Exception as e:
            traceback.print_exc()
            return common_response(400, str(e))


class FeaturedPlaceListAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PlaceDetailsSerializer

    def get(self, request):
        try:
            featured_places = Place.objects.filter(featured=True, is_available=True)
            serializer = self.serializer_class(
                featured_places, many=True, context={"request": request}
            )
            if request.accepted_renderer.format == "api":
                return Response(serializer.data)
            return common_response(
                200, "Featured places fetched successfully.", serializer.data
            )
        except Exception as e:
            return common_response(400, str(e))


class PlaceDetailsAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PlaceDetailsSerializer

    def get(self, request, slug):
        try:
            place = Place.objects.get(slug=slug)
            serializer = self.serializer_class(place, context={"request": request})
            if request.accepted_renderer.format == "api":
                return Response(serializer.data)
            return common_response(
                200, "Place details fetched successfully.", serializer.data
            )
        except Place.DoesNotExist:
            return common_response(404, "Place not found.")
        except Exception as e:
            return common_response(400, str(e))


class ToggleBookmarkPlaceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        try:
            place = Place.objects.get(slug=slug)
            user = request.user

            if place.owner == user:
                return common_response(400, "You cannot bookmark your own place.")

            if place in user.bookmarks.all():
                user.bookmarks.remove(place)
                return common_response(200, "Place removed from bookmarks.")
            else:
                user.bookmarks.add(place)
                return common_response(200, "Place added to bookmarks.")
        except Place.DoesNotExist:
            return common_response(404, "Place not found.")
        except Exception as e:
            return common_response(400, str(e))


class PlaceReviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        try:
            place = Place.objects.filter(slug=slug).first()
            if not place:
                return common_response(404, "Place not found.")

            if place.owner == request.user:
                return common_response(400, "You cannot review your own place.")

            if PlaceReview.objects.filter(place=place, reviewer=request.user).exists():
                return common_response(400, "You have already reviewed this place.")

            data = request.data.copy()
            data["place"] = place.id
            data["reviewer"] = request.user.id
            serializer = PlaceReviewCreateUpdateSerializer(data=data)
            if serializer.is_valid():
                review = serializer.save()
                return common_response(
                    201,
                    "Review created successfully.",
                    PlaceReviewCreateUpdateSerializer(review).data,
                )
            else:
                return common_response(400, "Invalid data.", serializer.errors)
        except Exception as e:
            traceback.print_exc()
            return common_response(400, str(e))

    def patch(self, request, slug):
        try:
            place = Place.objects.filter(slug=slug).first()
            if not place:
                return common_response(404, "Place not found.")

            review = PlaceReview.objects.filter(
                place=place, reviewer=request.user
            ).first()
            if not review:
                return common_response(404, "Review not found.")

            serializer = PlaceReviewCreateUpdateSerializer(
                review, data=request.data, partial=True
            )
            if serializer.is_valid():
                review = serializer.save()
                return common_response(
                    200,
                    "Review updated successfully.",
                    PlaceReviewCreateUpdateSerializer(review).data,
                )
            else:
                return common_response(400, "Invalid data.", serializer.errors)
        except Exception as e:
            traceback.print_exc()
            return common_response(400, str(e))
