import traceback

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination

from utils.responses import common_response
from user.helpers import (
    user_registration_service,
    otp_verification_service,
    user_login_service,
    forget_password_service,
    resend_otp_service,
)
from user.models import *
from user.serializers import *

from place.serializer import PlaceDetailsSerializer


class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
    page_query_param = "page"


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer_data = UserRegistrationSerializer(data=request.data)
            serializer_data.is_valid(raise_exception=True)
            payload = serializer_data.validated_data
            user = user_registration_service(payload)
            serializ_user = UserProfileSerializer(user)
            user = serializ_user.data

            return common_response(200, "User Registered Successfully", user)
        except Exception as e:
            return common_response(400, str(e))


class RegisterUserOTPVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer_data = RegisterUserOTPVerificationSerializer(data=request.data)
            serializer_data.is_valid(raise_exception=True)
            payload = serializer_data.validated_data
            verified = otp_verification_service(payload)

            if not verified:
                return common_response(400, "Invalid OTP")

            return common_response(200, "User Registered Successfully")
        except Exception as e:
            return common_response(400, str(e))


class LoginUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UserLoginSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            payload = serializer.validated_data
            response = user_login_service(payload, request)

            return common_response(200, "User Logged In Successfully", response)
        except Exception as e:
            return common_response(400, str(e))


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return common_response(200, "Password changed successfully.")


class ForgetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = EmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            payload = serializer.validated_data
            forget_password_service(payload)

            return common_response(200, "OTP sent successfully.")
        except Exception as e:
            return common_response(400, str(e))


class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = ResetPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return common_response(200, "Password reset successfully.")
        except Exception as e:
            return common_response(400, str(e))


class ResendOTPAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = EmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            payload = serializer.validated_data
            forget_password_service(payload)

            return common_response(200, "OTP sent successfully.")
        except Exception as e:
            return common_response(400, str(e))


class SendOTPEmailAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = EmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            payload = serializer.validated_data
            resend_otp_service(payload)

            return common_response(200, "OTP sent successfully.")
        except Exception as e:
            return common_response(400, str(e))


class LogoutUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return common_response(400, "Refresh token is required.")

            token = RefreshToken(refresh_token)
            token.blacklist()

            return common_response(200, "User Logged Out Successfully")
        except Exception as e:
            return common_response(400, str(e))


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            serializer = UserProfileSerializer(
                request.user, context={"request": request}
            )
            user = serializer.data
            return common_response(200, "User Profile fetched successfully.", user)
        except Exception as e:
            return common_response(400, str(e))


class UpdateProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # print(request.data)
            serializer = UpdataProfileSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return common_response(
                200, "User Profile updated successfully.", serializer.data
            )
        except Exception as e:
            traceback.print_exc()
            return common_response(400, str(e))


class HasAppliedForLandlordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            landlord_application = LandlordApplication.objects.filter(
                user=request.user
            ).first()
            if landlord_application:
                data = {
                    "is_landlord": landlord_application.status == "APPROVED",
                    "has_applied": landlord_application.status == "PENDING",
                    "application_date": landlord_application.application_date,
                    "status": landlord_application.status,
                    "rejection_reason": landlord_application.rejection_reason,
                }
                return common_response(200, "Landlord Application exists.", data)
            return common_response(200, "Landlord Application does not exist.")
        except Exception as e:
            return common_response(400, str(e))


class LandlordApplicationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = {}
            data["user"] = request.user.id
            data["status"] = "PENDING"
            data["application_date"] = timezone.now()
            serializer = LandlordApplicationSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return common_response(200, "Landlord Application submitted successfully.")
        except Exception as e:
            return common_response(400, str(e))


class UserNotificationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            notifications = Notification.objects.filter(user=request.user).order_by(
                "-created_at"
            )
            serializer = NotificationSerializer(notifications, many=True)
            return common_response(
                200, "Notifications fetched successfully.", serializer.data
            )
        except Exception as e:
            return common_response(400, str(e))


class UpdateNotificationReadStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = UpdateNotificationReadStatusSerializer(
                data=request.data,
                context={"request": request},  # Pass request context for user access
            )
            serializer.is_valid(raise_exception=True)
            result = serializer.save()

            return common_response(
                200,
                "Notification status updated successfully.",
                data={
                    "updated_count": result["updated_count"],
                    "processed_ids": result["notification_ids"],
                },
            )
        except ValidationError as e:
            return common_response(400, str(e))
        except Exception as e:
            return common_response(500, f"An unexpected error occurred: {str(e)}")


class MarkAllNotificationsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            with transaction.atomic():
                updated_count = Notification.objects.filter(
                    user=request.user, is_read=False
                ).update(is_read=True)

                return common_response(
                    200,
                    f"All notifications marked as read. Updated {updated_count} notifications.",
                    data={"updated_count": updated_count},
                )
        except Exception as e:
            return common_response(
                500, f"Failed to mark all notifications as read: {str(e)}"
            )


class ListedPropertiesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            properties = user.owned_places.order_by("-created_at")
            pagination = Pagination()
            properties = pagination.paginate_queryset(properties, request)
            serializer = PlaceDetailsSerializer(
                properties, many=True, context={"request": request}
            )
            return pagination.get_paginated_response(serializer.data)
        except Exception as e:
            return common_response(400, str(e))


class AboutHostAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            user = User.objects.filter(id=pk).first()
            if not user:
                return common_response(404, "User not found.")

            serializer = AboutHostSerializer(user, context={"request": request})
            return common_response(
                200, "User profile fetched successfully.", serializer.data
            )
        except Exception as e:
            return common_response(400, str(e))


# Task APIs
class TaskCreationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data.copy()
            print(data, "--------------------------------")
            data["user"] = request.user.id
            serializer = TaskCreationSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return_data = TaskSerializer(
                serializer.instance, context={"request": request}
            )
            return common_response(
                200, "Task created successfully.", data=return_data.data
            )
        except Exception as e:
            traceback.print_exc()
            return common_response(400, str(e))


class TaskUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            task = Task.objects.filter(id=pk).first()
            if not task:
                return common_response(404, "Task not found.")

            if task.user != request.user:
                return common_response(
                    403, "You are not authorized to update this task."
                )

            serializer = TaskSerializer(task, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = TaskSerializer(task, context={"request": request}).data
            return common_response(200, "Task updated successfully.", data=data)
        except Exception as e:
            traceback.print_exc()
            return common_response(400, str(e))


class TaskDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            task = Task.objects.filter(id=pk).first()
            if not task:
                return common_response(404, "Task not found.")

            if task.user != request.user:
                return common_response(
                    403, "You are not authorized to delete this task."
                )

            task.delete()
            return common_response(200, "Task deleted successfully.")
        except Exception as e:
            return common_response(400, str(e))


class TaskListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            tasks = Task.objects.filter(user=request.user).order_by("-created_at")
            serializer = TaskSerializer(tasks, many=True, context={"request": request})
            return common_response(200, "Tasks fetched successfully.", serializer.data)
        except Exception as e:
            return common_response(400, str(e))


class TaskToggleCompletedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            task = Task.objects.filter(id=pk).first()
            if not task:
                return common_response(404, "Task not found.")

            if task.user != request.user:
                return common_response(
                    403, "You are not authorized to update this task."
                )

            task.is_complete = not task.is_complete
            task.save()

            return common_response(200, "Task status updated successfully.")
        except Exception as e:
            return common_response(400, str(e))
