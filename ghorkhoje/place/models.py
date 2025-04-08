from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from user.models import User
from utils.functions import validate_image_size, unique_image_path
from place.configs import AppointmentStatus


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"ID:{self.id}, Name: {self.name}"

    class Meta:
        db_table = "categories"
        verbose_name_plural = "Categories"


class Facility(models.Model):
    name = models.CharField(max_length=255)
    bill = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"ID:{self.id}, Name: {self.name}"

    class Meta:
        db_table = "facilities"
        verbose_name_plural = "Facilities"


class Place(TimestampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True, null=True)
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
    num_prepayment_months = models.IntegerField(null=True, blank=True)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        db_index=True,
    )
    longitude = models.DecimalField(max_digits=9, decimal_places=6, db_index=True)
    area_in_sqft = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    num_of_bedrooms = models.IntegerField(default=1)
    num_of_bathrooms = models.IntegerField(default=1)
    num_of_balconies = models.IntegerField(default=0)
    num_of_kitchens = models.IntegerField(default=0)
    num_of_living_rooms = models.IntegerField(default=0)
    num_of_dining_rooms = models.IntegerField(default=0)
    num_of_parking_spaces = models.IntegerField(default=0)

    capacity = models.IntegerField(default=1)

    appointment_status = models.CharField(
        choices=AppointmentStatus.CHOICES,
        max_length=50,
        default=AppointmentStatus.APPOINTMENT_NON,
    )
    available_from = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(verbose_name="Archived", default=False)
    is_approved = models.BooleanField(verbose_name="Approved", default=False)

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

    def save(self, *args, **kwargs):
        if not self.slug:  # Auto-generate slug only if it's empty
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Place.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=["latitude", "longitude"]),
        ]
        db_table = "places"

    def __str__(self):
        return f"ID:{self.id}, Title: {self.title}, City: {self.city}"


class Image(TimestampedModel):
    place = models.ForeignKey(Place, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=unique_image_path,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"]),
            validate_image_size,
        ],
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Image for Place ID {self.place.id}"
