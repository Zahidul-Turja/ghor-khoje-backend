from django.db import models

from place.models import Place
from user.models import User
from booking.configs import PaymentMethods, PaymentStatus


class Booking(models.Model):
    place = models.ForeignKey(Place, related_name="bookings", on_delete=models.CASCADE)
    booked_by = models.ForeignKey(
        User, related_name="bookings", on_delete=models.CASCADE
    )
    payment_method = models.IntegerField(
        choices=PaymentMethods.CHOICES,
        default=1,
        blank=True,
    )
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    payment_status = models.IntegerField(
        choices=PaymentStatus.CHOICES, default=1, blank=True, null=True
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bookings"
        verbose_name_plural = "Bookings"
        indexes = [
            models.Index(fields=["place", "booked_by"]),
            models.Index(fields=["payment_status"]),
        ]

    def __str__(self):
        return f"Booking {self.id} | Place: {self.place.title} | User: {self.booked_by.username}"
