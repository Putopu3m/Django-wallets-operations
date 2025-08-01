from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import Operation, Wallet


def apply_operation(wallet: Wallet, operation_type: str, amount: Decimal) -> None:
    with transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(pk=wallet.pk)

        if amount < 0:
            raise ValidationError("Amount must be positive")

        if operation_type == Operation.OperationChoices.WITHDRAW:
            if wallet.amount < amount:
                raise ValidationError("Not enough money for the withdraw")

            wallet.amount -= amount
        elif operation_type == Operation.OperationChoices.DEPOSIT:
            wallet.amount += amount
        else:
            raise ValidationError("Invalid operation type")

        wallet.save()
