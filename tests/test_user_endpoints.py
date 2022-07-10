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


@pytest.mark.parametrize(
    "field,expected_field",
    [
        ("firstname", "Novo Nome"),
        ("surname", "Novo Sobrenome"),
        ("email", "novoemail@email.com.br"),
        ("cellphone", "88888888888"),
        ("document", "88888888888"),
        ("birthdate", "2022-08-10"),
    ],
)
def test_update_user(user, session, user_client, field, expected_field):
    session.add(user)
    session.commit()

    data = {field: expected_field}

    response = user_client.update(id=user.id_user, update=json.dumps(data))
    assert response.status_code == 200
    assert response.json()[field] == expected_field


def test_delete_user(user, session, user_client):
    session.add(user)
    session.commit()

    user_client.delete(id=user.id_user)
    response = user_client.get_by_id(id=user.id_user)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_user_by_id(user, session, user_client):
    session.add(user)
    session.commit()
    response = user_client.get_by_id(id=user.id_user)
    assert response.status_code == 200
    assert response.json()["id_user"] == str(user.id_user)
