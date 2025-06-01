from django.http import JsonResponse
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination

from booking.serilizers import *
from place.models import Place

import traceback


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# Create your views here.
class BookingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data.copy()
            data["booked_by"] = request.user.id
            place = Place.objects.filter(id=request.data.get("place")).first()
            if not place:
                place = Place.objects.filter(slug=request.data.get("place")).first()
            if not place:
                return JsonResponse(
                    {"status": "failed", "message": "Place not found."}, status=404
                )
            if not place.is_available:
                return JsonResponse(
                    {
                        "status": "failed",
                        "message": "This place is already booked or not available.",
                    },
                )

            contract_duration = int(request.data.get("contract_duration", 6))
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
                {
                    "status": "success",
                    "message": "Booking created successfully.",
                    "data": serializer.data,
                }
            )
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"message": str(e)}, status=500)


class BookingRequestListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            bookings = Booking.objects.filter(place__owner=user).order_by("-created_at")
            if not bookings:
                return JsonResponse(
                    {"status": "failed", "message": "No booking requests found."},
                )

            paginator = StandardResultsSetPagination()
            paginated_bookings = paginator.paginate_queryset(bookings, request)
            serializer = BookingRequestListSerializer(
                paginated_bookings, many=True, context={"request": request}
            )

            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"message": str(e)}, status=500)


class BookingRequestDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        try:
            booking = Booking.objects.filter(id=booking_id).first()
            if not booking:
                return JsonResponse(
                    {"status": "failed", "message": "Booking not found."}, status=404
                )

            serializer = BookingRequestListSerializer(
                booking, context={"request": request}
            )
            return JsonResponse(
                {"status": "success", "data": serializer.data}, status=200
            )
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"message": str(e)}, status=500)
