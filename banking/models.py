import secrets
from django.conf import settings
from django.db import models
from django.db.models import Q

def create_account_number():
    return "SB" + str(secrets.randbelow(90000000) + 10000000)

class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="account")
    account_number = models.CharField(max_length=10, unique=True, default=create_account_number)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=10000.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"

class Transaction(models.Model):
    reference = models.CharField(max_length=16, unique=True)
    from_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="debits")
    to_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="credits")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=120, default="Demo fund transfer")

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(condition=Q(amount__gt=0), name="transaction_amount_positive"),
        ]

    def __str__(self):
        return f"{self.reference} - {self.amount}"
