from django.db import models

from place.models import Place
from user.models import User


# Create your models here.
class Booking(models.Model):
    BOOKING_STATUS = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    place = models.ForeignKey(Place, related_name="bookings", on_delete=models.CASCADE)
    booked_by = models.ForeignKey(
        User, related_name="bookings", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bookings"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return f"ID: {self.id}, Place: {self.place.title}, Booked By: {self.booked_by.email}"
