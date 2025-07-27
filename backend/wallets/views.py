from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from decimal import Decimal

from .models import Wallet, Operation
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
    lookup_url_kwarg = 'wallet_id'
    permission_classes = [IsAuthenticated, IsWalletOwner]


class WalletOperationView(views.APIView):
    permission_classes = [IsAuthenticated, IsWalletOwner]

    def patch(self, request: Request, wallet_id):
        operation_type = request.data['operation_type']
        amount = Decimal(request.data["amount"])
        wallet = get_object_or_404(Wallet, pk=wallet_id)
        new_amount = apply_operation(wallet, request.user, operation_type, amount)
        operation = Operation.objects.create(
            wallet=wallet,
            user=request.user,
            operation_type=operation_type,
            amount=new_amount
        )
        serialized_wallet = WalletSerializer(wallet)
        return Response(serialized_wallet.data)

    