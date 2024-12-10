from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from booking.serilizers import BookingSerializer
from place.models import Place


# Create your views here.
class BookingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                place = Place.objects.get(id=request.data["place"])
                place.is_available = False
                place.appointment_status = "APPOINTMENT_CREATED"
                place.save()
                serializer.save()

            return JsonResponse(
                {"message": "Booking created successfully.", "data": serializer.data}
            )
        except Exception as e:
            return JsonResponse({"message": str(e)})
