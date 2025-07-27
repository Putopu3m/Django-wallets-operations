from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Wallet
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


class WalletOperationView(generics.GenericAPIView):
    pass

    