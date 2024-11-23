from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from place.models import Place, Facility, Category, Image
from place.serializer import PlaceSerializer, FacilitySerializer, CategorySerializer
from utils.responses import common_response


class FacilityAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            facilities = Facility.objects.all()
            serializer = FacilitySerializer(facilities, many=True)
            return common_response(
                200, "Facilities fetched successfully.", serializer.data
            )
        except Exception as e:
            return common_response(400, str(e))


class CategoryAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return common_response(
                200, "Categories fetched successfully.", serializer.data
            )
        except Exception as e:
            return common_response(400, str(e))


class PlaceAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get(self, request):
        try:
            places = Place.objects.all()
            serializer = PlaceSerializer(places, many=True)
            return common_response(200, "Places fetched successfully.", serializer.data)
        except Exception as e:
            return common_response(400, str(e))

    def post(self, request):
        try:
            serializer = PlaceSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return common_response(200, "Place created successfully.", serializer.data)
        except Exception as e:
            return common_response(400, str(e))
