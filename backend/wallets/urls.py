from django.urls import path
from .views import WalletDetailView, WalletOperationView

urlpatterns = [
    path("api/v1/wallets/<uuid:wallet_id>", WalletDetailView.as_view(), name="wallet-detail"),
    path("api/v1/wallets/<uuid:wallet_id>/operation", WalletOperationView.as_view(), name="wallet-operation"),
]
