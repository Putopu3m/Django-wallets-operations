import threading
from decimal import Decimal

import pytest
from django.db import connection
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User
from wallets.models import Operation, Wallet


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(django_user_model: User):
    return django_user_model.objects.create_user(username="user1", password="pass123")


@pytest.fixture
def user2(django_user_model: User):
    return django_user_model.objects.create_user(username="user2", password="pass456")


@pytest.fixture
def auth_client(client: APIClient, user: User):
    response = client.post(
        "/auth/token/", {"username": "user1", "password": "pass123"}, format="json"
    )
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def auth_client2(client: APIClient, user2: User):
    response = client.post(
        "/auth/token/", {"username": "user2", "password": "pass456"}, format="json"
    )
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def wallet(user: User):
    wallet = Wallet.objects.create(amount=0)
    wallet.users.add(user)
    return wallet


@pytest.mark.django_db
def test_create_wallet(auth_client: APIClient):
    response = auth_client.post(reverse("wallet-list-create"))
    assert response.status_code == status.HTTP_201_CREATED
    assert "wallet_id" in response.data or "id" in response.data


@pytest.mark.django_db
def test_get_wallet_balance(auth_client: APIClient, wallet: Wallet):
    response = auth_client.get(
        reverse("wallet-detail", kwargs={"wallet_id": wallet.pk})
    )
    assert response.status_code == status.HTTP_200_OK
    assert "amount" in response.data


@pytest.mark.django_db
def test_deposit_operation(auth_client: APIClient, wallet: Wallet):
    url = reverse("wallet-operation", kwargs={"wallet_id": wallet.pk})
    response = auth_client.post(url, {"operation_type": "DEPOSIT", "amount": "100.00"})
    assert response.status_code == status.HTTP_200_OK
    wallet.refresh_from_db()
    assert str(wallet.amount) == "100.00"


@pytest.mark.django_db
def test_withdraw_operation(auth_client: APIClient, wallet: Wallet):
    wallet.amount = 150
    wallet.save()

    url = reverse("wallet-operation", kwargs={"wallet_id": wallet.pk})
    response = auth_client.post(url, {"operation_type": "WITHDRAW", "amount": "50.00"})
    assert response.status_code == status.HTTP_200_OK
    wallet.refresh_from_db()
    assert str(wallet.amount) == "100.00"


@pytest.mark.django_db
def test_withdraw_not_enough_money(auth_client: APIClient, wallet: Wallet):
    url = reverse("wallet-operation", kwargs={"wallet_id": wallet.pk})
    response = auth_client.post(url, {"operation_type": "WITHDRAW", "amount": "100.00"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Not enough money" in response.data["detail"]


@pytest.mark.django_db
def test_access_denied_to_other_user_wallet(auth_client2: APIClient, wallet: Wallet):
    url = reverse("wallet-detail", kwargs={"wallet_id": wallet.pk})
    response = auth_client2.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_operations_list(auth_client: APIClient, wallet: Wallet, user: User):
    Operation.objects.create(
        wallet=wallet, user=user, operation_type="DEPOSIT", amount=100
    )
    Operation.objects.create(
        wallet=wallet, user=user, operation_type="WITHDRAW", amount=50
    )

    url = reverse("operation-list")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db(transaction=True)
def test_concurrent_withdrawals(user, auth_client):
    wallet = Wallet.objects.create(amount=Decimal("100.00"))
    wallet.users.add(user)

    url = reverse("wallet-operation", kwargs={"wallet_id": wallet.pk})

    num_threads = 5
    withdraw_amount = Decimal("10.00")

    def make_withdraw():
        try:
            response = auth_client.post(
                url,
                {"operation_type": "WITHDRAW", "amount": str(withdraw_amount)},
                format="json",
            )
            assert response.status_code in [
                status.HTTP_200_OK,
                status.HTTP_400_BAD_REQUEST,
            ]
        finally:
            connection.close()

    threads = [threading.Thread(target=make_withdraw) for _ in range(num_threads)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    wallet.refresh_from_db()
    operations_count = wallet.operations.count()
    expected_balance = Decimal("100.00") - withdraw_amount * operations_count

    assert wallet.amount == expected_balance
    assert operations_count <= num_threads


@pytest.mark.django_db(transaction=True)
def test_concurrent_deposits(user, auth_client):
    wallet = Wallet.objects.create(amount=Decimal("100.00"))
    wallet.users.add(user)

    url = reverse("wallet-operation", kwargs={"wallet_id": wallet.pk})

    num_threads = 5
    deposit_amount = Decimal("10.00")

    def make_withdraw():
        try:
            response = auth_client.post(
                url,
                {"operation_type": "DEPOSIT", "amount": str(deposit_amount)},
                format="json",
            )
            assert response.status_code == status.HTTP_200_OK
        finally:
            connection.close()

    # Запуск потоков
    threads = [threading.Thread(target=make_withdraw) for _ in range(num_threads)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    expected_balance = wallet.amount + deposit_amount * num_threads
    wallet.refresh_from_db()
    assert (
        wallet.amount == expected_balance
    ), f"Expected: {expected_balance}, Actual: {wallet.amount}"
