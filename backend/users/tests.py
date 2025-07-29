import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_user_registration(client: APIClient):
    response = client.post(
        "/auth/register/", {"username": "testuser", "password": "pass123"}
    )
    assert response.status_code == 201
    assert User.objects.filter(username="testuser").exists()


@pytest.mark.django_db
def test_user_registration_existing_username(client: APIClient):
    User.objects.create_user(username="testuser", password="pass123")
    response = client.post(
        "/auth/register/", {"username": "testuser", "password": "newpass"}
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_registration_missing_fields(client: APIClient):
    response = client.post("/auth/register/", {"username": "useronly"})
    assert response.status_code == 400

    response = client.post("/auth/register/", {"password": "passonly"})
    assert response.status_code == 400


@pytest.mark.django_db
def test_token_obtain_success(client: APIClient):
    User.objects.create_user(username="testuser", password="pass123")
    response = client.post(
        "/auth/token/", {"username": "testuser", "password": "pass123"}
    )
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_token_obtain_fail_wrong_password(client: APIClient):
    User.objects.create_user(username="testuser", password="pass123")
    response = client.post(
        "/auth/token/", {"username": "testuser", "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert "access" not in response.data
