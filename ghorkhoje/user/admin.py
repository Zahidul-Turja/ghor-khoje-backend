from django.utils.html import format_html
from django.contrib import admin

from user.models import *

# Register your models here.


class ReviewInline(admin.TabularInline):
    model = Review
    fk_name = "reviewee"
    extra = 0


class UserAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
    list_display = ("id", "full_name", "email", "phone", "user_type")
    exclude = ("password", "user_permissions")
    list_filter = ("user_type", "is_deleted")
    search_fields = ("full_name", "email", "phone")
    ordering = ("-created_at",)
    list_per_page = 20


class LandlordAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "application_date", "updated_at")
    list_filter = ("status",)
    search_fields = ("user__full_name", "user__email")
    ordering = ("-application_date",)
    readonly_fields = ("applicant_info", "application_date", "updated_at")
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Allow superusers to see all
        return qs.filter(user=request.user)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "status",
                    "rejection_reason",
                    "application_date",
                    "updated_at",
                )
            },
        ),
        (
            "Applicant Details",
            {
                "fields": ("applicant_info",),
            },
        ),
    )

    def applicant_info(self, obj):
        user = obj.user
        return format_html(
            f"""
            <div style="line-height: 1.6;">
                <strong>Name:</strong> {user.full_name}<br>
                <strong>Email:</strong> {user.email}<br>
                <strong>Phone:</strong> {user.phone}<br>
                <strong>Gender:</strong> {user.gender}<br>
                <strong>Date of Birth:</strong> {user.date_of_birth}<br>
                <strong>Profession:</strong> {user.profession}<br>
                <strong>NID:</strong> {user.nid}<br>
                <strong>User Type:</strong> {user.user_type}<br>
                {"<br><img src='{}' width='100' style='border-radius: 8px;' />".format(user.profile_image.url) if user.profile_image else ""}
            </div>
            """
        )

    applicant_info.short_description = "Applicant Info"


class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "is_read", "created_at")
    search_fields = ("user__full_name", "user__email")
    ordering = ("-created_at",)
    list_per_page = 40


admin.site.register(User, UserAdmin)
admin.site.register(LandlordApplication, LandlordAdmin)
admin.site.register(Notification, NotificationAdmin)
