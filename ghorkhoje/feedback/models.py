from django.db import models


# Create your models here.
class FeedbackType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Feedback Types"


class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, related_name="feedbacks"
    )
    feedback_type = models.ForeignKey(
        FeedbackType, on_delete=models.CASCADE, related_name="feedbacks"
    )
    email = models.EmailField(blank=True)
    name = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    want_to_be_contacted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} - {self.name} ({self.email})"

    class Meta:
        verbose_name_plural = "Feedbacks"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
            models.Index(fields=["feedback_type"]),
        ]
