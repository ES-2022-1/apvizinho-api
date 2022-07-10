import json

import pytest

from .base_client import BaseClient

ADDRESS = {
            "street": "Avenida Manoel Tavares",
            "city": "Campina Grande",
            "number": "1065",
            "complement": "Próximo a pizzaria dominos",
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
    data = {
        "title":"Casarão Universitário",
        "description": "Casa espaçosa próxima à UFCG",
        "is_close_to_university": True,
        "is_close_to_supermarket": True,
        "has_furniture": True,
        "has_internet": True,
        "allow_pet": False,
        "allow_events": False,
        "has_piped_gas": True,
        "type": "HOUSE",
        "status": "ACTIVE",
        "address": {
            "street": "Silva Barbosa",
            "city": "Campina Grande",
            "number": "975",
            "complement": "Próximo à UFCG",
            "zip_code": "58400-825"
        },
        "rooms": [
            {
                "has_bathroom": True, 
                "has_garage": False ,
                "has_furniture": True,
                "has_cable_internet": True,
                "is_shared_room": True,
                "allowed_smoker": False,
                "required_organized_person": True,
                "required_extroverted_person": True,
                "gender":"FEMALE",
                "price":500

            }
        ]
        }

    response = local_client.create(json.dumps(data))

    assert response.status_code == 200
    assert response.json()["tittle"] == "Casarão Universitário"

@pytest.mark.parametrize(
    "field,expected_field",
    [
        ("tittle", "Nova Casa"),
        ("description", "Nova descrição"),
        ("is_close_to_university", True),
        ("is_close_to_supermarket", False),
        ("has_furniture", False),
        ("has_internet", True),
        ("allow_pet", True),
        ("allow_events", True),
        ("has_piped_gas", False),
        ("type", "HOUSE"),
        ("status", "DISABLED"),
        ("address", ADDRESS),
        ("rooms", ROOMS)
    ],
)
def test_update_local(local, session, local_client, field, expected_field):
    session.add(local)
    session.commit()

    data = {field: expected_field}

    response = local_client.update(id=local.id_local, update=json.dumps(data))
    assert response.status_code == 200
    assert response.json()[field] == expected_field


def test_delete_local(local, session, local_client):
    session.add(local)
    session.commit()

    local_client.delete(id=local.id_local)
    response = local_client.get_by_id(id=local.id_local)
    assert response.status_code == 404
    assert response.json()["detail"] == "Local not found"


def test_get_local_by_id(local, session, local_client):
    session.add(local)
    session.commit()
    response = local_client.get_by_id(id=local.id_local)
    assert response.status_code == 200
    assert response.json()["id_local"] == str(local.id_local)


def test_list_locals(local, session, local_client):
    session.add(local)
    session.commit()
    response = local_client.get_all()

    assert response.status_code == 200
    assert len(response.json()) == 1

