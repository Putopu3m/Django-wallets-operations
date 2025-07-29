from django.urls import path

from .views import (OperationsListView, WalletDetailView, WalletListCreateView,
                    WalletOperationView)

urlpatterns = [
    path("", WalletListCreateView.as_view(), name="wallet-list-create"),
    path("<uuid:wallet_id>/", WalletDetailView.as_view(), name="wallet-detail"),
    path(
        "<uuid:wallet_id>/operation/",
        WalletOperationView.as_view(),
        name="wallet-operation",
    ),
    path("operations/", OperationsListView.as_view(), name="operation-list"),
]
