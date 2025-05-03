from django.contrib import admin

from place.models import Place, Category, Facility, Image

# Register your models here.


class ImageAdmin(admin.TabularInline):
    model = Image
    extra = 0


class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]
    list_display = ("id", "title", "owner", "city", "category", "created_at")
    list_filter = ("city", "category", "created_at")
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


admin.site.register(Place, PlaceAdmin)
admin.site.register(Image)
