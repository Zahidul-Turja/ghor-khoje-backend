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
            serializer = FacilitySerializer(facilities, many=True)
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
            serializer = CategorySerializer(categories, many=True)
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
            places = Place.objects.all()
            paginator = self.pagination_class()
            paginated_places = paginator.paginate_queryset(places, request)
            serializer = PlaceSerializer(paginated_places, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return common_response(400, str(e))


class PlaceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            print(request.data, "-------------------------------------")
            data = request.data.copy()

            serializer = PlaceSerializer(data=data, context={"request": request})
            if serializer.is_valid(raise_exception=True):
                place = serializer.create(serializer.validated_data)
                return common_response(
                    201, "Place created successfully.", PlaceSerializer(place).data
                )
            else:
                return common_response(400, "Invalid data.", serializer.errors)
        except Exception as e:
            traceback.print_exc()
            return common_response(400, str(e))


class PlaceDetailsAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PlaceSerializer

    def get(self, request, slug):
        try:
            place = Place.objects.get(slug=slug)
            serializer = PlaceSerializer(place)
            if request.accepted_renderer.format == "api":
                return Response(serializer.data)
            return common_response(
                200, "Place details fetched successfully.", serializer.data
            )
        except Place.DoesNotExist:
            return common_response(404, "Place not found.")
        except Exception as e:
            return common_response(400, str(e))
