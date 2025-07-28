from decimal import Decimal

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.exceptions import ValidationError
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
        try:
            operation_type = request.data["operation_type"]
            amount = Decimal(request.data["amount"])
            try:
                wallet = get_object_or_404(Wallet, pk=wallet_id)
            except Http404 as error:
                return Response(
                    {"detail": "Object not found."}, status=status.HTTP_404_NOT_FOUND
                )
            apply_operation(wallet, operation_type, amount)
            Operation.objects.create(
                wallet=wallet,
                user=request.user,
                operation_type=operation_type,
                amount=amount,
            )

            return Response(WalletSerializer(wallet).data)
        except ValidationError as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)


class OperationsListView(generics.ListAPIView):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.operations.all()
