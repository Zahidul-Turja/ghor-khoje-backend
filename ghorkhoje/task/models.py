from django.db import models
from django.db.models import TextChoices
from user.models import User


# Create your models here.
class TaskCategory(TextChoices):
    maintenance = "Maintenance"
    cleaning = "Cleaning"
    guest_relations = "Guest Relations"
    financial = "Financial"
    marketing = "Marketing"
    other = "Other"


class TaskPriority(TextChoices):
    high = "High"
    medium = "Medium"
    low = "Low"


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=50, choices=TaskCategory.choices, default=TaskCategory.other
    )
    priority = models.CharField(
        max_length=50, choices=TaskPriority.choices, default=TaskPriority.low
    )
    due_date = models.DateField(blank=True, null=True)
    related_property = models.ForeignKey(
        "place.Place", on_delete=models.CASCADE, null=True, blank=True
    )

    is_complete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Task for {self.user} - {self.title}"

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        db_table = "tasks"
