from django.http import HttpResponse
from django.views.decorators.http import require_GET

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from user.models import Review
from ghorkhoje.serializers import ReviewSerializer


class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Okay"}, status=status.HTTP_200_OK)


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
            },
            status=status.HTTP_200_OK,
        )


@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",  # keep crawlers off the Django admin entirely
        "Disallow: /api/v1/auth/",  # sensitive endpoints
        "Allow: /api/v1/public/",  # public endpoints stay crawlable
        "",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
