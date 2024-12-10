from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from utils.responses import common_response
from ghorkhoje.user.helpers import (
    user_registration_service,
    otp_verification_service,
    user_login_service,
    forget_password_service,
)
from user.serializers import (
    UserRegistrationSerializer,
    RegisterUserOTPVerificationSerializer,
    UserLoginSerializer,
    ChangePasswordSerializer,
    EmailOrPhoneSerializer,
    ResetPasswordSerializer,
)


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer_data = UserRegistrationSerializer(data=request.data)
            serializer_data.is_valid(raise_exception=True)
            payload = serializer_data.validated_data
            user_registration_service(payload)

            return common_response(200, "User Registered Successfully")
        except Exception as e:
            return common_response(400, str(e))
        return common_response(200, "User Registered Successfully", request.data)


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
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            payload = serializer.validated_data
            response = user_login_service(payload)

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
            serializer = EmailOrPhoneSerializer(data=request.data)
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
