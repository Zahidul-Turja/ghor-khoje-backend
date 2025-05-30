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
    # STATUS_CHOICES = [
    #     ("new", "New"),
    #     ("in_progress", "In Progress"),
    #     ("resolved", "Resolved"),
    #     ("closed", "Closed"),
    #     ("archived", "Archived"),
    #     ("deleted", "Deleted"),
    #     ("spam", "Spam"),
    #     ("flagged", "Flagged"),
    #     ("important", "Important"),
    #     ("feature_request", "Feature Request"),
    #     ("bug_report", "Bug Report"),
    #     ("complaint", "Complaint"),
    #     ("suggestion", "Suggestion"),
    # ]
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, related_name="feedbacks", default=1
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
    # is_resolved = models.BooleanField(default=False)
    # is_public = models.BooleanField(default=True)
    # is_anonymous = models.BooleanField(default=False)
    # is_archived = models.BooleanField(default=False)
    # is_deleted = models.BooleanField(default=False)
    # is_spam = models.BooleanField(default=False)
    # is_flagged = models.BooleanField(default=False)
    # is_important = models.BooleanField(default=False)
    # is_feature_request = models.BooleanField(default=False)
    # is_bug_report = models.BooleanField(default=False)
    # is_complaint = models.BooleanField(default=False)
    # is_suggestion = models.BooleanField(default=False)

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
