from django.contrib import admin

from booking.models import Booking


# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "place",
        "booked_by",
        "payment_status",
        "payment_method",
        "created_at",
    )
    search_fields = ("place__title", "booked_by__username")
    list_filter = ("payment_status", "payment_method", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
