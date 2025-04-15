from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db.models import Avg

from user.configs import UserTypes, Gender


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
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
        upload_to="users/profile_images/", null=True, blank=True
    )
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
        result = self.received_reviews.aggregate(avg_rating=Avg("rating"))
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
    rating = models.IntegerField(null=True, blank=True)
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

    def __str__(self):
        return f"Application by {self.user} - Status: {self.status}"
