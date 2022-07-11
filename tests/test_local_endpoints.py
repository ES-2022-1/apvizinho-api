import json

import pytest
from tests.conftest import client

from .base_client import BaseClient
from .test_user_endpoints import UserClient

ADDRESS = {
            "street": "Avenida Manoel Tavares",
            "city": "Campina Grande",
            "number": "1065",
            "complement": "Proximo a pizzaria dominos",
            "zip_code": " 58401-402"
        }

ROOMS = [
    {
        "has_bathroom": True, 
        "has_garage": False ,
        "has_furniture": False,
        "has_cable_internet": False,
        "is_shared_room": True,
        "allowed_smoker": False,
        "required_organized_person": True,
        "required_extroverted_person": True,
        "gender": 'MALE',
        "price": 400
    }               
]

class LocalClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="local")


@pytest.fixture
def local_client(client):
    return LocalClient(client)


@pytest.fixture
def local(make_local):
    return make_local()


def test_create_local(local_client):
    data_user = {
        "firstname": "Nome",
        "surname": "Sobrenome",
        "email": "email@email.com.br",
        "cellphone": "99999999999",
        "document": "99999999999",
        "birthdate": "2022-07-10",
        "password": "SEGREDO!",
    }
    user_client = UserClient(client)
    response = user_client.create(json.dumps(data_user))
    id_user = response.json()["id_user"]

    data = {
            "title": "Casa maravilhosa",
            "description": "casarao",
            "is_close_to_university": True,
            "is_close_to_supermarket": True,
            "has_furniture": True,
            "has_internet": True,
            "allow_pet": True,
            "allow_events": True,
            "has_piped_gas": True,
            "status": "ACTIVE",
            "type": "HOUSE",
            "id_user": id_user,
            "address": ADDRESS,
            "rooms": ROOMS
}           
    response = local_client.create(json.dumps(data))

    assert response.status_code == 200
    assert response.json()["tittle"] == "Casa maravilhosa"

# @pytest.mark.parametrize(
#     "field,expected_field",
#     [
#         ("tittle", "Nova Casa"),
#         ("description", "Nova descrição"),
#         ("is_close_to_university", True),
#         ("is_close_to_supermarket", False),
#         ("has_furniture", False),
#         ("has_internet", True),
#         ("allow_pet", True),
#         ("allow_events", True),
#         ("has_piped_gas", False),
#         ("type", "HOUSE"),
#         ("status", "DISABLED"),
#         ("address", ADDRESS),
#         ("rooms", ROOMS)
#     ],
# )
# def test_update_local(local, session, local_client, field, expected_field):
#     session.add(local)
#     session.commit()

#     data = {field: expected_field}

#     response = local_client.update(id=local.id_local, update=json.dumps(data))
#     assert response.status_code == 200
#     assert response.json()[field] == expected_field


# def test_delete_local(local, session, local_client):
#     session.add(local)
#     session.commit()

#     local_client.delete(id=local.id_local)
#     response = local_client.get_by_id(id=local.id_local)
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Local not found"


# def test_get_local_by_id(local, session, local_client):
#     session.add(local)
#     session.commit()
#     response = local_client.get_by_id(id=local.id_local)
#     assert response.status_code == 200
#     assert response.json()["id_local"] == str(local.id_local)


# def test_list_locals(local, session, local_client):
#     session.add(local)
#     session.commit()
#     response = local_client.get_all()

#     assert response.status_code == 200
#     assert len(response.json()) == 1

