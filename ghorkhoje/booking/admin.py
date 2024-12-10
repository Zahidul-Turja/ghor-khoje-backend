from django.contrib import admin

from booking.models import Booking


# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "place", "booked_by", "status")
    list_filter = ("status",)
    search_fields = ("place__title", "booked_by__username")
    ordering = ("-created_at",)
