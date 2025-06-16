from django.urls import path

from user.views import *

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
    path("resend-otp/", ResendOTPAPIView.as_view(), name="resend_otp"),
    path("send-otp-email/", SendOTPEmailAPIView.as_view(), name="send_otp_email"),
]

user_urlpatterns = [
    path("profile/", UserProfileAPIView.as_view(), name="user_profile"),
    path("profile/update/", UpdateProfileAPIView.as_view(), name="user_profile"),
    path("notifications/", UserNotificationAPIView.as_view(), name="user_notification"),
    path(
        "has-applied-for-landlord/",
        HasAppliedForLandlordAPIView.as_view(),
        name="has_applied_for_landlord",
    ),
    path(
        "listed-properties/",
        ListedPropertiesAPIView.as_view(),
        name="listed_properties",
    ),
    path(
        "notifications/mark-read/",
        UpdateNotificationReadStatusAPIView.as_view(),
        name="mark-notifications-read",
    ),
    path(
        "notifications/mark-all-read/",
        MarkAllNotificationsReadAPIView.as_view(),
        name="mark-all-notifications-read",
    ),
    path("tasks/create/", TaskCreationAPIView.as_view(), name="create_task"),
    path("about-host/<int:pk>/", AboutHostAPIView.as_view(), name="about_host"),
]

application_urlpatterns = [
    path(
        "landlord/",
        LandlordApplicationAPIView.as_view(),
        name="landlord_application",
    ),
    # path("send-email-test/", SendEmailTestView.as_view(), name="send_email_test"),
]
