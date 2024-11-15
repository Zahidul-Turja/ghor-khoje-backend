from django.urls import path

from user.views import RegisterUserView, RegisterUserOTPVerificationView, LoginUserView

app_name = "user"

auth_urlpatterns = [
    path("registration/", RegisterUserView.as_view(), name="register_user"),
    path(
        "registration-verification/otp/",
        RegisterUserOTPVerificationView.as_view(),
        name="register_user_otp",
    ),
    path("login/", LoginUserView.as_view(), name="login_user"),
]
