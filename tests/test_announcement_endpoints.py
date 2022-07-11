import json

import pytest

from .base_client import BaseClient


class AnnouncementClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="announcement")


@pytest.fixture
def announcement_client(client):
    return AnnouncementClient(client)


@pytest.fixture
def make_full_local(make_local, make_room):
    local = make_local()
    rooms = make_room(local=local)

    return {"local": local, "rooms": [rooms]}


def test_create_announcement(make_user, announcement_client, session):
    user = make_user()
    session.add(user)
    session.commit()

    data = {
        "title": "string",
        "description": "string",
        "is_close_to_university": True,
        "is_close_to_supermarket": True,
        "has_furniture": True,
        "has_internet": True,
        "allow_pet": True,
        "allow_events": True,
        "has_piped_gas": True,
        "status": "ACTIVE",
        "type": "HOUSE",
        "id_user": user.id_user,
        "address": {
            "street": "Avenida Marechal Floraino Peixoto",
            "city": "Campina Grande",
            "number": "5255",
            "complement": "Lote B06",
            "zip_code": "585434500",
        },
        "vacancies": [
            {
                "has_bathroom": True,
                "has_garage": True,
                "has_furniture": True,
                "has_cable_internet": True,
                "is_shared_room": True,
                "allowed_smoker": True,
                "required_organized_person": True,
                "required_extroverted_person": True,
                "gender": "FEMALE",
                "price": 0,
            }
        ],
    }

    response = announcement_client.create(json.dumps(data))

    assert response.status_code == 200
    assert response.json()["title"] == "string"
