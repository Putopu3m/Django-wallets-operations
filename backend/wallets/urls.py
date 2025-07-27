from django.urls import path

from .views import WalletDetailView, WalletListCreateView, WalletOperationView

urlpatterns = [
    path('', WalletListCreateView.as_view(), name='wallet_list_create'),
    path("<uuid:wallet_id>/", WalletDetailView.as_view(), name="wallet_detail"),
    path("<uuid:wallet_id>/operation/", WalletOperationView.as_view(), name="wallet_operation"),
]
