from django.http import JsonResponse
import requests
from random import randint

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user.models import Review
from ghorkhoje.serializers import ReviewSerializer


def get_random_quote(request):
    return JsonResponse({"status": "success", "message": "Welcome to GhorKhojee API"})
    quote_number = randint(1, 1400)
    url = f"https://dummyjson.com/quotes/{quote_number}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        return JsonResponse(data)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


class GeneralReviews(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        reviews = Review.objects.filter(overall=5).order_by("-created_at")[:10]
        serialized_reviews = ReviewSerializer(
            reviews, many=True, context={"request": request}
        )
        review_data = serialized_reviews.data

        return Response(
            {
                "status": "success",
                "message": "Reviews fetched successfully.",
                "data": review_data,
            }
        )
