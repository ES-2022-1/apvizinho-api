import json

import pytest

from .base_client import BaseClient


class UserClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="user")


@pytest.fixture
def user_client(client):
    return UserClient(client)


@pytest.fixture
def user(make_user):
    return make_user()


def test_create_user(user_client):
    data = {
        "firstname": "Nome",
        "surname": "Sobrenome",
        "email": "email@email.com.br",
        "cellphone": "99999999999",
        "document": "99999999999",
        "birthdate": "2022-07-10",
        "password": "SEGREDO!",
    }

    response = user_client.create(json.dumps(data))

    assert response.status_code == 200
    assert response.json()["firstname"] == "Nome"
