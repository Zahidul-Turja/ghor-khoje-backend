from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db.models import Avg
from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models import TextChoices
from django.core.validators import MinValueValidator, MaxValueValidator

from cloudinary_storage.storage import MediaCloudinaryStorage

from user.configs import UserTypes, Gender


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields["is_active"] = True
        extra_fields["is_staff"] = True

        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)

        try:
            group, created = Group.objects.get_or_create(name="application_admin")
            user.groups.add(group)
        except Exception as e:
            print(e)
            pass
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name="email address", max_length=255, unique=True, null=True, blank=True
    )
    phone = models.CharField(max_length=14, null=True, blank=True, unique=True)
    profile_image = models.ImageField(
        upload_to="users/profile_images/",
        storage=(
            MediaCloudinaryStorage() if settings.ENVIRONMENT == "production" else None
        ),
        null=True,
        blank=True,
    )
    cover_image = models.ImageField(
        upload_to="users/cover_images/",
        storage=(
            MediaCloudinaryStorage() if settings.ENVIRONMENT == "production" else None
        ),
        null=True,
        blank=True,
    )
    bio = models.TextField(null=True, blank=True)
    gender = models.CharField(
        choices=Gender.CHOICES,
        default=Gender.MALE,
        max_length=10,
        null=True,
        blank=True,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    nid = models.CharField(max_length=20, null=True, blank=True)
    user_type = models.CharField(
        max_length=20, choices=UserTypes.CHOICES, default=UserTypes.BACHELOR
    )
    otp = models.CharField(max_length=6, null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)

    languages = models.CharField(max_length=255, null=True, blank=True)
    preferred_language = models.CharField(max_length=255, null=True, blank=True)

    # Social Media Links
    linkedin = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)

    bookmarks = models.ManyToManyField(
        "place.Place", related_name="bookmarks", blank=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(
        default=False, help_text="Soft delete: whether this user is archived or not."
    )

    objects = CustomUserManager()
    USERNAME_FIELD = "email"

    def get_average_rating(self):
        result = self.received_reviews.aggregate(avg_rating=Avg("overall"))
        return (
            round(result["avg_rating"], 2) if result["avg_rating"] is not None else None
        )

    def get_average_communication_rating(self):
        result = self.received_reviews.aggregate(avg_rating=Avg("communication"))
        return (
            round(result["avg_rating"], 2) if result["avg_rating"] is not None else None
        )

    def get_average_cleanliness_rating(self):
        result = self.received_reviews.aggregate(avg_rating=Avg("cleanliness"))
        return (
            round(result["avg_rating"], 2) if result["avg_rating"] is not None else None
        )

    def get_average_maintenance_rating(self):
        result = self.received_reviews.aggregate(avg_rating=Avg("maintenance"))
        return (
            round(result["avg_rating"], 2) if result["avg_rating"] is not None else None
        )

    def get_average_privacy_rating(self):
        result = self.received_reviews.aggregate(avg_rating=Avg("privacy"))
        return (
            round(result["avg_rating"], 2) if result["avg_rating"] is not None else None
        )

    def get_average_financial_transparency_rating(self):
        result = self.received_reviews.aggregate(
            avg_rating=Avg("financial_transparency")
        )
        return (
            round(result["avg_rating"], 2) if result["avg_rating"] is not None else None
        )

    def get_average_attitude_rating(self):
        result = self.received_reviews.aggregate(avg_rating=Avg("attitude"))
        return (
            round(result["avg_rating"], 2) if result["avg_rating"] is not None else None
        )

    def get_review_count(self):
        return self.received_reviews.count()

    def __str__(self):
        return self.email if self.email else self.phone


class Review(models.Model):
    reviewer = models.ForeignKey(
        User,
        related_name="given_reviews",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    reviewee = models.ForeignKey(
        User,
        related_name="received_reviews",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    communication = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
    )
    cleanliness = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
    )
    maintenance = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
    )
    privacy = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
    )
    financial_transparency = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
    )
    attitude = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
    )
    overall = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
    )
    review_text = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.reviewer} to {self.reviewee} - Rating: {self.rating}"


class LandlordApplication(models.Model):
    STATUS = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )
    user = models.ForeignKey(
        User, related_name="landlord_applications", on_delete=models.CASCADE
    )
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS, default="PENDING", null=True, blank=True
    )
    rejection_reason = models.TextField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-application_date"]
        verbose_name = "Landlord Application"
        verbose_name_plural = "Landlord Applications"

    def save(self, *args, **kwargs):
        if self.status == "APPROVED":
            self.user.user_type = UserTypes.LANDLORD
            self.user.save()

            Notification.objects.create(
                user=self.user,
                message="Your landlord application has been approved.",
            )
        elif self.status == "REJECTED":
            self.user.user_type = UserTypes.BACHELOR
            self.user.save()
            Notification.objects.create(
                user=self.user,
                message=f"Your landlord application has been rejected. Reason: {self.rejection_reason}",
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Application by {self.user} - Status: {self.status}"


class Notification(models.Model):
    STATUS = (
        ("PENDING", "Pending"),
        ("READ", "Read"),
        ("ARCHIVED", "Archived"),
        ("DELETED", "Deleted"),
        ("UNREAD", "Unread"),
    )
    TYPE = (
        ("SYSTEM", "System"),
        ("BOOKING", "Booking"),
        ("REVIEW", "Review"),
        ("SUCCESS", "Success"),
        ("ERROR", "Error"),
        ("WARNING", "Warning"),
        ("INFO", "Info"),
        ("OTHER", "Other"),
    )
    user = models.ForeignKey(
        User, related_name="notifications", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=50, default="SYSTEM", choices=TYPE)
    status = models.CharField(max_length=50, default="PENDING", choices=STATUS)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - {self.message[:20]}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"


# Tasks
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
