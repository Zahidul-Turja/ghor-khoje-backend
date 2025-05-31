from django.db import models

from place.models import Place
from user.models import User


# Create your models here.
class Booking(models.Model):
    BOOKING_STATUS = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
        ("no_show", "No Show"),
        ("refunded", "Refunded"),
        ("waiting_for_payment", "Waiting for Payment"),
        ("payment_failed", "Payment Failed"),
    ]

    place = models.ForeignKey(Place, related_name="bookings", on_delete=models.CASCADE)
    booked_by = models.ForeignKey(
        User, related_name="bookings", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default="pending")

    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    move_in_date = models.DateField(blank=True, null=True)
    move_out_date = models.DateField(blank=True, null=True)
    number_of_occupants = models.PositiveIntegerField(default=1)
    note = models.TextField(blank=True, null=True)

    rent_per_month = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    extra_bills = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    num_prepayment_months = models.IntegerField(null=True, blank=True)
    latitude = models.DecimalField(
        max_digits=25, decimal_places=15, db_index=True, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=25, decimal_places=15, db_index=True, null=True, blank=True
    )
    area_in_sqft = models.IntegerField(null=True, blank=True)

    agreed_to_terms = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bookings"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return f"ID: {self.id}, Place: {self.place.title}, Booked By: {self.booked_by.email}"
