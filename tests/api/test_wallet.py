import pytest
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from wallet.models import Transaction
import json


@pytest.mark.django_db
def test_user_post_transaction(client, user, user_token):

    payload = {
      "amount": "20.00",
      "category": "Машина",
      "organization": "Автосервис",
      "description": "Замена масла двигателя",
      "income": False
    }

    response = client.post('/api/v1/transaction/', payload,
                           HTTP_AUTHORIZATION=f"{user_token}", format='json')

    data = response.data
    user.refresh_from_db()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["amount"] == payload["amount"]
    assert data["category"] == payload["category"]
    assert data["organization"] == payload["organization"]
    # make sure the user balance changed after transaction
    assert data["amount"] == str(-user.balance)


@pytest.mark.django_db
def test_user_get_his_transactions(client_with_transactions, transaction,
                                   another_transaction, user_token):

    response = client_with_transactions.get('/api/v1/transaction/',
                                            HTTP_AUTHORIZATION=f"{user_token}",
                                            format='json')

    data = json.loads(json.dumps(response.data))

    assert response.status_code == status.HTTP_200_OK
    assert data["results"][0]["amount"] == transaction["amount"]
    assert data["results"][0]["category"] == transaction["category"]
    assert data["results"][1]["organization"] == another_transaction["organization"]
    assert data["results"][1]["income"] == another_transaction["income"]


@pytest.mark.django_db
def test_user_get_detail_transaction(client_with_transactions, transaction,
                                     user_token, transaction_id):

    response = client_with_transactions.get(f'/api/v1/transaction/{transaction_id}/',
                                            HTTP_AUTHORIZATION=f"{user_token}",
                                            format='json')

    data = response.data

    assert response.status_code == status.HTTP_200_OK
    assert data["amount"] == transaction["amount"]
    assert data["category"] == transaction["category"]
    assert data["organization"] == transaction["organization"]


@pytest.mark.django_db
def test_user_change_detail_transaction(client_with_transactions,
                                     user_token, transaction_id):

    payload = {
        "amount": "60.00",
        "category": "Машина",
        "organization": "Автосервис",
        "description": "Замена масла двигателя",
        "income": False
    }

    response = client_with_transactions.put(f'/api/v1/transaction/{transaction_id}/',
                                            payload,
                                            HTTP_AUTHORIZATION=f"{user_token}",
                                            format='json')

    data = response.data

    assert response.status_code == status.HTTP_200_OK
    assert data["amount"] == payload["amount"]
    assert data["category"] == payload["category"]
    assert data["organization"] == payload["organization"]


@pytest.mark.django_db
def test_user_forbidden_detailed_transaction(client_with_transactions,
                                             user_token,
                                             superuser_transaction_id):

    response = client_with_transactions.get(f'/api/v1/transaction/{superuser_transaction_id}/',
                                            HTTP_AUTHORIZATION=f"{user_token}",
                                            format='json')

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_transaction_delete(client_with_transactions, user_token, transaction_id):

    transaction_to_delete = Transaction.objects.get(pk=transaction_id)

    response = client_with_transactions.delete(f"/api/v1/transaction/{transaction_id}/", {},
                                               HTTP_AUTHORIZATION=f"{user_token}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    with pytest.raises(ObjectDoesNotExist):
        transaction_to_delete.refresh_from_db()
