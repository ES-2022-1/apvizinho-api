import json

import pytest

from .base_client import BaseClient


class SessionClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="session")


class UserClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="user")


@pytest.fixture
def session_client(client):
    return SessionClient(client)


@pytest.fixture
def user_client(client):
    return UserClient(client)


@pytest.fixture
def user(user_client):
    user_primary_data = {"email": "email@email.com.br", "password": "SEGREDO!"}

    data = {
        "firstname": "Nome",
        "surname": "Sobrenome",
        "email": user_primary_data["email"],
        "cellphone": "99999999999",
        "document": "99999999999",
        "birthdate": "2022-07-10",
        "password": user_primary_data["password"],
    }

    user_client.create(json.dumps(data))

    return user_primary_data


def test_create_session(user, session_client):
    email = user["email"]
    password = user["password"]

    data = {"email": email, "password": password}

    response = session_client.create(json.dumps(data))
    assert response.status_code == 200


def test_create_session_with_nonexistent_user(user, session_client):
    email = "email@gmail.com"
    password = user["password"]

    data = {"email": email, "password": password}

    response = session_client.create(json.dumps(data))
    assert response.status_code == 404
    assert response.json()["detail"] == f"User with email {email} not found"


def test_create_session_with_wrong_password(user, session_client):
    email = user["email"]
    password = "senhaErrada"

    data = {"email": email, "password": password}

    response = session_client.create(json.dumps(data))
    assert response.status_code == 401
    assert response.json()["detail"] == "Wrong password"
