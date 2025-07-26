from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Wallet
from .serializers import WalletSerializer, OperationSerializer
from .permissions import IsWalletOwner
from .services import apply_operation

class WalletDetailView(generics.RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_url_kwarg = 'wallet_id'
    permission_classes = [IsAuthenticated, IsWalletOwner]

    