from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from user.models import User
from utils.functions import validate_image_size


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"ID:{self.id}, Name: {self.name}"


class Facility(models.Model):
    name = models.CharField(max_length=255)
    bill = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"ID:{self.id}, Name: {self.name}"


class Place(TimestampedModel):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, related_name="owned_places", on_delete=models.CASCADE
    )
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        related_name="places",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
    )
    facilities = models.ManyToManyField(Facility, related_name="places", blank=True)
    city = models.CharField(max_length=255)
    area_name = models.CharField(max_length=255)
    area_code = models.CharField(max_length=20, null=True, blank=True)
    block_name = models.CharField(max_length=10, null=True, blank=True)
    street_name = models.CharField(max_length=40, null=True, blank=True)
    house_name = models.CharField(max_length=50, null=True, blank=True)
    house_number = models.CharField(max_length=10, null=True, blank=True)
    apartment_number = models.CharField(max_length=10, null=True, blank=True)
    floor_number = models.CharField(max_length=5, null=True, blank=True)
    rent_per_month = models.DecimalField(max_digits=12, decimal_places=2)
    extra_bills = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        db_index=True,
    )
    longitude = models.DecimalField(max_digits=9, decimal_places=6, db_index=True)

    def clean(self):
        if not (20.5 <= self.latitude <= 26.6):
            raise ValidationError(
                f"Latitude {self.latitude} is out of bounds for Bangladesh (20.5°N to 26.6°N)."
            )
        if not (88.0 <= self.longitude <= 92.7):
            raise ValidationError(
                f"Longitude {self.longitude} is out of bounds for Bangladesh (88.0°E to 92.7°E)."
            )

        if self.rent_per_month < 0:
            raise ValidationError("Rent per month cannot be negative.")

    def __str__(self):
        return f"ID:{self.id}, Title: {self.title}"


class Image(TimestampedModel):
    place = models.ForeignKey(Place, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="places/",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"]),
            validate_image_size,
        ],
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Image for Place ID {self.place.id}"
