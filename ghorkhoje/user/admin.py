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
    list_filter = ("user_type", "is_deleted")
    search_fields = ("full_name", "email", "phone")
    ordering = ("-created_at",)
    list_per_page = 20


admin.site.register(User, UserAdmin)
