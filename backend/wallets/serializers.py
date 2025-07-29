from rest_framework import serializers

from .models import Operation, Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("wallet_id", "amount")


class OperationSerializer(serializers.Serializer):
    operation_type = serializers.ChoiceField(choices=Operation.OperationChoices.choices)
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)

