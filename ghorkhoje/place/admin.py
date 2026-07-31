from django.contrib import admin

from place.models import *


class ImageAdmin(admin.TabularInline):
    model = Image
    extra = 0


class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]
    list_display = ("id", "slug", "title", "owner", "city", "category")
    list_display_links = ("id", "slug", "title")
    list_filter = ("category",)
    search_fields = ("title", "owner__username", "city")
    search_help_text = "Search by title, owner's username or city"
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "slug")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ("name",)
    search_fields = ("name",)


class PlaceReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "place", "reviewer", "overall", "created_at")
    list_display_links = ("id", "place", "reviewer", "overall")
    list_filter = ("place", "reviewer", "created_at")
    search_fields = ("place__title", "reviewer__username")
    ordering = ("-created_at",)


admin.site.register(Place, PlaceAdmin)
admin.site.register(Image)
admin.site.register(PlaceReview, PlaceReviewAdmin)
