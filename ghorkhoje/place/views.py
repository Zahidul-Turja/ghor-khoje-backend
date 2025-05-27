import traceback

import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination

from place.models import *
from place.serializer import *
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


class PlaceListAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PlaceDetailsSerializer
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        try:
            category_slug = request.query_params.get("category")
            category = Category.objects.filter(slug=category_slug).first()
            places = (
                Place.objects.filter(category=category)
                if category_slug != "all"
                else Place.objects.all()
            )
            paginator = self.pagination_class()
            paginated_places = paginator.paginate_queryset(places, request)
            serializer = self.serializer_class(
                paginated_places, many=True, context={"request": request}
            )
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return common_response(400, str(e))


class PlaceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            print(request.data, "-------------------------------------")
            data = request.data.copy()
            # Normalize scalar fields (convert single-item lists to strings/numbers)
            normalized_data = {
                key: value[0] if isinstance(value, list) else value
                for key, value in data.lists()
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
                return common_response(
                    201,
                    "Place created successfully.",
                    PlaceDetailsSerializer(place).data,
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
