import json

import pytest

from app.announcement.schemas.announcement import AnnouncementTypeEnum, StatusEnum

from .base_client import BaseClient


class AnnouncementClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="announcement")


@pytest.fixture
def client(client):
    return AnnouncementClient(client)


@pytest.fixture
def announcement(make_announcement):
    return make_announcement()


def test_create_announcement(make_user, client, session):
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

    response = client.create(json.dumps(data))

    assert response.status_code == 200
    assert response.json()["title"] == "string"


@pytest.mark.parametrize(
    "field,expected_field",
    [
        ("title", "Novo Titulo"),
        ("description", "Nova Descricao"),
        ("is_close_to_university", False),
        ("is_close_to_supermarket", False),
        ("has_furniture", False),
        ("has_internet", False),
        ("allow_pet", False),
        ("allow_events", False),
        ("has_piped_gas", False),
        ("type", AnnouncementTypeEnum.APARTMENT),
        ("status", StatusEnum.DISABLED),
    ],
)
def test_update_announcement(announcement, session, client, field, expected_field):
    session.add(announcement)
    session.commit()

    data = {field: expected_field}

    response = client.update(id=announcement.id_announcement, update=json.dumps(data))
    assert response.status_code == 200
    assert response.json()[field] == expected_field
