import pytest
from rest_framework.test import APIClient

from user.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(client):
    payload = {
        "email": "bilbo_baggins@shire.com",
        "password": "youshallnotpass",
    }

    response = client.post("/api/v1/user/", payload)

    data = response.data

    user = User.objects.get(email=data["email"])

    return user


@pytest.fixture
def superuser():
    payload = {
        "email": "geralt_of_rivia@neverland.com",
        "password": "thewitcher",
    }

    user = User.objects.create_superuser(**payload)

    return user


@pytest.fixture
def user_token(client, user):
    payload = {
        "email": user,
        "password": "youshallnotpass"
    }
    response = client.post("/api/v1/user/login/", data=payload)
    token = response.data["token"]

    return token


@pytest.fixture
def superuser_token(client, superuser):
    payload = {
        "email": superuser,
        "password": "thewitcher"
    }
    response = client.post("/api/v1/user/login/", data=payload)

    token = response.data["token"]

    return token
