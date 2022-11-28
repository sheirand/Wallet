import json
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


@pytest.fixture
def transaction():

    transaction = {
      "amount": "20.00",
      "category": "Машина",
      "organization": "Автосервис",
      "description": "Замена масла двигателя",
      "income": False
    }

    return transaction


@pytest.fixture
def another_transaction():
    transaction = {
        "amount": "50.00",
        "category": "Зарплата",
        "organization": "Завод",
        "description": "Еще немного денег, чтобы дожить до следующей зарплаты",
        "income": True
    }

    return transaction


@pytest.fixture
def client_with_transactions(client, user_token, transaction, another_transaction):

    client.post('/api/v1/transaction/', transaction,
                HTTP_AUTHORIZATION=f"{user_token}", format="json")

    client.post('/api/v1/transaction/', another_transaction,
                HTTP_AUTHORIZATION=f"{user_token}", format="json")

    client.post('/api/v1/transaction/', transaction,
                HTTP_AUTHORIZATION=f"{superuser_token}", format="json")

    return client


@pytest.fixture
def transaction_id(client_with_transactions, user_token):

    response = client_with_transactions.get('/api/v1/transaction/',
                                            HTTP_AUTHORIZATION=f"{user_token}",
                                            format='json')

    data = json.loads(json.dumps(response.data))

    return data["results"][0]["id"]


@pytest.fixture
def superuser_transaction_id(client_with_transactions, superuser_token):

    response = client_with_transactions.get('/api/v1/transaction/',
                                            HTTP_AUTHORIZATION=f"{superuser_token}",
                                            format='json')

    data = json.loads(json.dumps(response.data))

    return data["results"][0]["id"]
