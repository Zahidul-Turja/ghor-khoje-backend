class PaymentMethods:
    CASH = 1
    CARD = 2
    ONLINE = 3
    CHOICES = [
        (CASH, "Cash"),
        (CARD, "Card"),
        (ONLINE, "Online"),
    ]


class PaymentStatus:
    PENDING = 1
    COMPLETED = 2
    FAILED = 3

    CHOICES = [(PENDING, "Pending"), (COMPLETED, "Completed"), (FAILED, "Failed")]
