from django.contrib import admin

from place.models import *


class ImageAdmin(admin.TabularInline):
    model = Image
    extra = 0


class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]
    list_display = ("id", "title", "owner", "city", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "owner__username", "city")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "slug")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


class PlaceReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "place", "reviewer", "overall", "created_at")
    list_filter = ("place", "reviewer", "created_at")
    search_fields = ("place__title", "reviewer__username")
    ordering = ("-created_at",)


admin.site.register(Place, PlaceAdmin)
admin.site.register(Image)
admin.site.register(PlaceReview, PlaceReviewAdmin)
