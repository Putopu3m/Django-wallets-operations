from decimal import Decimal

from rest_framework import generics, status, views
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Operation, Wallet
from .permissions import IsWalletOwner
from .serializers import OperationSerializer, WalletSerializer
from .services import apply_operation


class WalletListCreateView(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.wallets.all()

    def perform_create(self, serializer):
        wallet = serializer.save()
        wallet.users.add(self.request.user)
        return super().perform_create(serializer)


class WalletDetailView(generics.RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_url_kwarg = "wallet_id"
    permission_classes = [IsAuthenticated, IsWalletOwner]


class WalletOperationView(views.APIView):
    permission_classes = [IsAuthenticated, IsWalletOwner]

    def post(self, request: Request, wallet_id):
        operation_type = request.data["operation_type"]
        amount = Decimal(request.data["amount"])
        wallet = get_object_or_404(Wallet, pk=wallet_id)

        if request.user not in wallet.users.all():
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        try:
            apply_operation(wallet, operation_type, Decimal(amount))
        except ValidationError as error:
            return Response({"detail": repr(error)}, status=status.HTTP_400_BAD_REQUEST)

        Operation.objects.create(
            wallet=wallet,
            user=request.user,
            operation_type=operation_type,
            amount=amount,
        )

        return Response(WalletSerializer(wallet).data)


class OperationsListView(generics.ListAPIView):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.operations.all()
