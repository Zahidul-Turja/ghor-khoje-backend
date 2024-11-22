from django.urls import path

from user.views import (
    RegisterUserView,
    RegisterUserOTPVerificationView,
    LoginUserAPIView,
    LogoutUserAPIView,
    ChangePasswordAPIView,
    ForgetPasswordAPIView,
    ResetPasswordAPIView,
)

app_name = "user"

auth_urlpatterns = [
    path("registration/", RegisterUserView.as_view(), name="register_user"),
    path(
        "registration-verification/otp/",
        RegisterUserOTPVerificationView.as_view(),
        name="register_user_otp",
    ),
    path("login/", LoginUserAPIView.as_view(), name="login_user"),
    path("logout/", LogoutUserAPIView.as_view(), name="logout_user"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change_password"),
    path("forget-password/", ForgetPasswordAPIView.as_view(), name="forget_password"),
    path("reset-password/", ResetPasswordAPIView.as_view(), name="reset_password"),
]
