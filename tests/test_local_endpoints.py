import json

import pytest

from .base_client import BaseClient


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

