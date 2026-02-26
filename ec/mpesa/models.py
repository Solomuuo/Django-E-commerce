from django.db import models
from django.utils.timezone import now

class MpesaTransaction(models.Model):
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_receipt_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=[("Pending", "Pending"), ("Completed", "Completed"), ("Failed", "Failed")],
        default="Pending"
    )
    transaction_date = models.DateTimeField(default=now)  # Auto set date

    def __str__(self):
        return f"{self.phone_number} - {self.amount} - {self.status}"