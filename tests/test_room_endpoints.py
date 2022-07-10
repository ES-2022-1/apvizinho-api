import json

import pytest

from .base_client import BaseClient


class RoomClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="room")


@pytest.fixture
def room_client(client):
    return RoomClient(client)


@pytest.fixture
def room(make_room):
    return make_room()


def test_create_room(room_client):
    data = {
        #ajustar
        "id_local": "ajjksjsjk",
        "has_bathroom": True, 
        "has_garage": True ,
        "has_furniture": False,
        "has_cable_internet": True,
        "is_shared_room": False,
        "allowed_smoker": False,
        "required_organized_person": True, 
        "required_ectroverted_person": False, 
        "gender":"feminino", 
        "price": "500" 
    }

    response = room_client.create(json.dumps(data))

    assert response.status_code == 200
    assert response.json()["price"] == "500"


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
def test_update_user(room, session, room_client, field, expected_field):
    session.add(room)
    session.commit()

    data = {field: expected_field}

    response = room_client.update(id=room.id_user, update=json.dumps(data))
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


def test_list_users(user, session, user_client):
    session.add(user)
    session.commit()
    response = user_client.get_all()

    assert response.status_code == 200
    assert len(response.json()) == 1
