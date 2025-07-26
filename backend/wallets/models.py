from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Wallet(models.Model):
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    users = models.ManyToManyField(User, related_name='accounts')

    def __str__(self):
        return f"Account {self.account_id} — {self.amount}"

class Operation(models.Model):
    class OperationChoices(models.TextChoices):
        DEPOSIT = 'DEPOSIT'
        WITHDRAW = 'WITHDRAW'

    operation_type = models.CharField(choices=OperationChoices.choices)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operations')
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='operations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.operation_type} {self.amount} on {self.bank_account} by {self.user}"
