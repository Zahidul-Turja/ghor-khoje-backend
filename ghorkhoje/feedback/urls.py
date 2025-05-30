from django.urls import path

from feedback.views import *

feedback_urlpatterns = [
    path(
        "feedback-types/",
        FeedbackTypeListView.as_view(),
        name="feedback_type_list",
    ),
    path(
        "status-list/",
        StatusListView.as_view(),
        name="status_list",
    ),
    path("give-feedback/", CreateFeedbackView.as_view(), name="create_feedback"),
    path("feedback-list/", FeedbackListView.as_view(), name="feedback_list"),
]
