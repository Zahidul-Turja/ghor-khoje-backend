from django.contrib import admin

from .models import Feedback, FeedbackType, Status


# Register your models here.
class FeedbackTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


class StatusAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "status",
        "feedback_type",
        "email",
        "name",
        "subject",
        "message",
        "want_to_be_contacted",
        "created_at",
        "updated_at",
    )
    search_fields = ("email", "name", "subject", "message")
    list_filter = ("status", "feedback_type", "want_to_be_contacted")
    ordering = ("-created_at",)


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(FeedbackType, FeedbackTypeAdmin)
admin.site.register(Status, StatusAdmin)
