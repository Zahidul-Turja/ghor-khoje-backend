class AppointmentStatus:
    APPOINTMENT_CREATED = "APPOINTMENT_CREATED"
    APPOINTMENT_ACCEPTED = "APPOINTMENT_ACCEPTED"
    APPOINTMENT_REJECTED = "APPOINTMENT_REJECTED"
    APPOINTMENT_CANCELLED = "APPOINTMENT_CANCELLED"
    APPOINTMENT_COMPLETED = "APPOINTMENT_COMPLETED"

    CHOICES = [
        (APPOINTMENT_CREATED, "Appointment Created"),
        (APPOINTMENT_ACCEPTED, "Appointment Accepted"),
        (APPOINTMENT_REJECTED, "Appointment Rejected"),
        (APPOINTMENT_CANCELLED, "Appointment Cancelled"),
        (APPOINTMENT_COMPLETED, "Appointment Completed"),
    ]
