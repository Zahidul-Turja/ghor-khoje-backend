from django.http import JsonResponse
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from booking.serilizers import BookingCreationSerializer
from place.models import Place


# Create your views here.
class BookingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data.copy()
            data["booked_by"] = request.user.id
            place = Place.objects.get(id=request.data["place"])
            contract_duration = int(request.data["contract_duration"])
            move_out_date = timezone.now().date() + relativedelta(
                months=contract_duration
            )
            data["move_out_date"] = move_out_date
            data["rent_per_month"] = place.rent_per_month
            data["extra_bills"] = place.extra_bills
            data["latitude"] = place.latitude
            data["longitude"] = place.longitude
            data["area_in_sqft"] = place.area_in_sqft

            serializer = BookingCreationSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                place.is_available = False
                place.appointment_status = "APPOINTMENT_CREATED"
                place.save()
                serializer.save()

            return JsonResponse(
                {"message": "Booking created successfully.", "data": serializer.data}
            )
        except Exception as e:
            return JsonResponse({"message": str(e)})
