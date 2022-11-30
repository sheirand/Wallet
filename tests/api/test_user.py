import jwt
import pytest
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from user.services import DEFAULT_CATEGORIES


@pytest.mark.django_db
def test_register_user(client):

    payload = {
        "email": "old_hobbit@shire.com",
        "password": "youshallnotpass"
    }

    response = client.post("/api/v1/user/", payload)

    data = response.data

    assert response.status_code == status.HTTP_201_CREATED
    assert data["categories"] == DEFAULT_CATEGORIES
    assert data["email"] == payload["email"]
    assert "password" not in data


@pytest.mark.django_db
def test_user_login(client, user):

    payload = {
        "email": user,
        "password": "youshallnotpass"
    }

    response = client.post("/api/v1/user/login/", data=payload)

    credentials = jwt.decode(response.data["token"],
                             settings.JWT_SECRET_KEY,
                             algorithms=['HS256'])

    assert response.status_code == status.HTTP_201_CREATED
    assert "token" in response.data
    assert user.email == credentials["email"]
    assert user.id == credentials["id"]


@pytest.mark.django_db
def test_get_user_info_by_superuser(client, user, superuser_token):

    response = client.get(f"/api/v1/user/{user.id}/", {},
                          HTTP_AUTHORIZATION=f"{superuser_token}")

    data = response.data

    assert response.status_code == status.HTTP_200_OK
    assert data["email"] == user.email
    assert data["categories"] == list(user.categories.values_list("name", flat=True))
    assert data["balance"] == str(user.balance)


@pytest.mark.django_db
def test_access_user_endpoint_by_user(client, user, user_token):

    response = client.get(f"/api/v1/user/{user.id}/", {},
                          HTTP_AUTHORIZATION=f"{user_token}")

    data = response.data
    print(user.id)
    assert response.status_code == status.HTTP_200_OK
    assert data["email"] == user.email
    assert data["categories"] == list(user.categories.values_list("name", flat=True))
    assert data["balance"] == str(user.balance)


@pytest.mark.django_db
def test_access_forbidden_another_user_detail(client, superuser, user_token):

    response = client.get(f"/api/v1/user/{superuser.id}/", {},
                          HTTP_AUTHORIZATION=f"{user_token}")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_change_categories(client, user, user_token):
    payload = {"categories": ["Пирожок с вишней", "Коньяк"]}

    response = client.patch(f"/api/v1/user/{user.id}/",
                            data=payload,
                            HTTP_AUTHORIZATION=f"{user_token}",
                            format="json")

    data = response.data
    assert response.status_code == status.HTTP_200_OK
    assert data["categories"] == list(user.categories.values_list("name", flat=True))


@pytest.mark.django_db
def test_user_delete(client, user, superuser_token):

    response = client.delete(f"/api/v1/user/{user.id}/", {},
                             HTTP_AUTHORIZATION=f"{superuser_token}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    with pytest.raises(ObjectDoesNotExist):
        user.refresh_from_db()
