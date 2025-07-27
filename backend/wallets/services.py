from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import Operation, Wallet


def apply_operation(account: Wallet, user, operation_type: str, amount: Decimal) -> Decimal:
    with transaction.atomic():
        account = Wallet.objects.select_for_update().get(pk=account.pk)

        if operation_type == Operation.OperationChoices.WITHDRAW:
            if account.amount < amount:
                raise ValidationError("Not enough money for the withdraw")

            account.amount -= amount
        elif operation_type == Operation.OperationChoices.DEPOSIT:
            account.amount += amount
        else:
            raise ValidationError("Invalid operation type")

        account.save()

        Operation.objects.create(
            bank_account=account,
            user=user,
            operation_type=operation_type,
            amount=amount
        )

        return account.amount
