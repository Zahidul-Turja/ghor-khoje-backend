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
    path(
        "deactivate-account/", DeactivateUserAPIView.as_view(), name="deactivate_user"
    ),
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
    path("bookmarks/", BookmarkListAPIView.as_view(), name="bookmark_list"),
    path(
        "ids-bookmarked-places/",
        IdsBookmarkedPlacesAPIView.as_view(),
        name="ids_bookmarked_places",
    ),
    path("tasks/", TaskListAPIView.as_view(), name="task_list"),
    path("tasks/create/", TaskCreationAPIView.as_view(), name="create_task"),
    path("tasks/update/<int:pk>/", TaskUpdateAPIView.as_view(), name="update_task"),
    path("tasks/delete/<int:pk>/", TaskDeleteAPIView.as_view(), name="delete_task"),
    path(
        "tasks/toggle-completed/<int:pk>/",
        TaskToggleCompletedAPIView.as_view(),
        name="toggle_task_completed",
    ),
    path("analytics/", UserAnalyticsAPIView.as_view(), name="user_analytics"),
    path("about-host/<int:pk>/", AboutHostAPIView.as_view(), name="about_host"),
    # Reviews
    path("review-user/<int:pk>/", ReviewUserAPIView.as_view(), name="review-user"),
    path(
        "review/update/<int:pk>/",
        ReviewUserAPIView.as_view(),
        name="update-review-user",
    ),
]

application_urlpatterns = [
    path(
        "landlord/",
        LandlordApplicationAPIView.as_view(),
        name="landlord_application",
    ),
    # path("send-email-test/", SendEmailTestView.as_view(), name="send_email_test"),
]
