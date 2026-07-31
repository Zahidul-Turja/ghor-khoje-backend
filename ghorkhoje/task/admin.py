from django.contrib import admin

from task.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "title",
        "description",
        "category",
        "priority",
        "due_date",
    )
    search_fields = ("user__full_name", "user__email")
    ordering = ("-created_at",)
    list_per_page = 40
