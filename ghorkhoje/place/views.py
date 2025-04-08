from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination

from place.models import Place, Facility, Category
from place.serializer import PlaceSerializer, FacilitySerializer, CategorySerializer
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
            facilities = Facility.objects.all()
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
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            if request.accepted_renderer.format == "api":
                return Response(serializer.data)
            return common_response(
                200, "Categories fetched successfully.", serializer.data
            )
        except Exception as e:
            return common_response(400, str(e))


class PlaceAPIView(APIView):
    serializer_class = PlaceSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get(self, request, *args, **kwargs):
        try:
            places = Place.objects.all()

            # Get paginator instance
            paginator = self.pagination_class()
            paginated_places = paginator.paginate_queryset(places, request)

            # Serialize paginated data
            serializer = PlaceSerializer(paginated_places, many=True)

            # Return paginated response
            paginated_response = paginator.get_paginated_response(serializer.data)

            # If you need to use your common_response format
            return common_response(
                200,
                "Places fetched successfully.",
                paginated_response.data,
            )
        except Exception as e:
            return common_response(400, str(e))

    def post(self, request, *args, **kwargs):
        try:
            serializer = PlaceSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return common_response(200, "Place created successfully.", serializer.data)
        except Exception as e:
            if request.accepted_renderer.format == "api":
                return Response({"error": str(e)}, status=400)
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
