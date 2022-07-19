import json
from uuid import UUID

import pytest

from app.announcement.schemas.announcement import (
    AnnouncementStatus,
    AnnouncementTagsEnum,
    AnnouncementTypeEnum,
)

from .base_client import BaseClient


class AnnouncementClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="announcement")

    def list_announcements_by_filter(self, announcement_filter):
        return self.client.post(
            f"{self.path}/filter", headers=self.headers, json=announcement_filter
        )

    def disable(self, id: UUID):
        return self.client.patch(f"/{self.path}/{str(id)}/disable", headers=self.headers)

    def enable(self, id: UUID):
        return self.client.patch(f"/{self.path}/{str(id)}/enable", headers=self.headers)


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
        ("status", AnnouncementStatus.DISABLED),
    ],
)
def test_update_announcement(announcement, session, client, field, expected_field):
    session.add(announcement)
    session.commit()

    data = {field: expected_field}

    response = client.update(id=announcement.id_announcement, update=json.dumps(data))
    assert response.status_code == 200
    assert response.json()[field] == expected_field


def test_delete_announcement(announcement, session, client):
    session.add(announcement)
    session.commit()

    client.delete(id=announcement.id_announcement)
    response = client.get_by_id(id=announcement.id_announcement)
    assert response.status_code == 404
    assert response.json()["detail"] == "Announcement not found"


def test_get_announcement_by_id(announcement, session, client):
    session.add(announcement)
    session.commit()
    response = client.get_by_id(id=announcement.id_announcement)
    assert response.status_code == 200
    assert response.json()["id_announcement"] == str(announcement.id_announcement)


def test_list_announcements(announcement, session, client):
    session.add(announcement)
    session.commit()
    response = client.get_all()

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_announcements_by_filter_1(make_user, session, client):
    user = make_user()
    session.add(user)
    session.commit()

    data_anuncio1 = {
        "title": "anuncio 1",
        "description": "string",
        "is_close_to_university": True,
        "is_close_to_supermarket": True,
        "has_furniture": False,
        "has_internet": False,
        "allow_pet": True,
        "allow_events": True,
        "has_piped_gas": False,
        "status": "ACTIVE",
        "type": "HOUSE",
        "id_user": user.id_user,
        "address": {
            "street": "Av. Ricardo Wagner da Silva Paz",
            "city": "Campina Grande",
            "number": "200",
            "complement": "",
            "zip_code": "58429110",
        },
        "vacancies": [
            {
                "has_bathroom": False,
                "has_garage": True,
                "has_furniture": False,
                "has_cable_internet": False,
                "is_shared_room": True,
                "allowed_smoker": False,
                "required_organized_person": False,
                "required_extroverted_person": False,
                "gender": "FEMALE",
                "price": 0,
            }
        ],
    }

    data_anuncio2 = {
        "title": "anuncio 2",
        "description": "string",
        "is_close_to_university": False,
        "is_close_to_supermarket": True,
        "has_furniture": True,
        "has_internet": False,
        "allow_pet": True,
        "allow_events": True,
        "has_piped_gas": False,
        "status": "ACTIVE",
        "type": "HOUSE",
        "id_user": user.id_user,
        "address": {
            "street": "Rua Bolivia",
            "city": "Campina Grande",
            "number": "380",
            "complement": "",
            "zip_code": "58416543",
        },
        "vacancies": [
            {
                "has_bathroom": False,
                "has_garage": False,
                "has_furniture": True,
                "has_cable_internet": False,
                "is_shared_room": False,
                "allowed_smoker": True,
                "required_organized_person": False,
                "required_extroverted_person": False,
                "gender": "FEMALE",
                "price": 0,
            }
        ],
    }

    data_anuncio3 = {
        "title": "anuncio 3",
        "description": "string",
        "is_close_to_university": True,
        "is_close_to_supermarket": True,
        "has_furniture": False,
        "has_internet": True,
        "allow_pet": True,
        "allow_events": True,
        "has_piped_gas": True,
        "status": "ACTIVE",
        "type": "HOUSE",
        "id_user": user.id_user,
        "address": {
            "street": "R. Antônio Joaquim Pequeno",
            "city": "Campina Grande",
            "number": "595",
            "complement": "",
            "zip_code": "58429105",
        },
        "vacancies": [
            {
                "has_bathroom": True,
                "has_garage": True,
                "has_furniture": True,
                "has_cable_internet": True,
                "is_shared_room": False,
                "allowed_smoker": False,
                "required_organized_person": True,
                "required_extroverted_person": False,
                "gender": "FEMALE",
                "price": 0,
            }
        ],
    }

    client.create(json.dumps(data_anuncio1))
    client.create(json.dumps(data_anuncio2))
    client.create(json.dumps(data_anuncio3))

    filters = {
        "filters": [
            AnnouncementTagsEnum.IS_CLOSE_TO_UNIVERSITY,
            AnnouncementTagsEnum.IS_CLOSE_TO_SUPERMARKET,
            AnnouncementTagsEnum.ALLOW_PETS,
            AnnouncementTagsEnum.FEMALE_GENDER,
        ]
    }

    response = client.list_announcements_by_filter(filters)

    assert response.status_code == 200
    assert list(map(lambda x: x["title"], response.json())) == [
        "anuncio 3",
        "anuncio 1",
        "anuncio 2",
    ]


def test_list_announcements_by_filter_2(make_user, session, client):
    user = make_user()
    session.add(user)
    session.commit()

    data_anuncio1 = {
        "title": "anuncio 1",
        "description": "string",
        "is_close_to_university": True,
        "is_close_to_supermarket": True,
        "has_furniture": False,
        "has_internet": False,
        "allow_pet": True,
        "allow_events": True,
        "has_piped_gas": False,
        "status": "ACTIVE",
        "type": "HOUSE",
        "id_user": user.id_user,
        "address": {
            "street": "Av. Ricardo Wagner da Silva Paz",
            "city": "Campina Grande",
            "number": "200",
            "complement": "",
            "zip_code": "58429110",
        },
        "vacancies": [
            {
                "has_bathroom": False,
                "has_garage": True,
                "has_furniture": False,
                "has_cable_internet": False,
                "is_shared_room": True,
                "allowed_smoker": False,
                "required_organized_person": False,
                "required_extroverted_person": False,
                "gender": "MALE",
                "price": 0,
            }
        ],
    }

    data_anuncio2 = {
        "title": "anuncio 2",
        "description": "string",
        "is_close_to_university": False,
        "is_close_to_supermarket": True,
        "has_furniture": True,
        "has_internet": False,
        "allow_pet": True,
        "allow_events": True,
        "has_piped_gas": False,
        "status": "ACTIVE",
        "type": "HOUSE",
        "id_user": user.id_user,
        "address": {
            "street": "Rua Bolivia",
            "city": "Campina Grande",
            "number": "380",
            "complement": "",
            "zip_code": "58416543",
        },
        "vacancies": [
            {
                "has_bathroom": False,
                "has_garage": False,
                "has_furniture": True,
                "has_cable_internet": False,
                "is_shared_room": False,
                "allowed_smoker": True,
                "required_organized_person": False,
                "required_extroverted_person": False,
                "gender": "FEMALE",
                "price": 0,
            }
        ],
    }

    data_anuncio3 = {
        "title": "anuncio 3",
        "description": "string",
        "is_close_to_university": True,
        "is_close_to_supermarket": True,
        "has_furniture": False,
        "has_internet": True,
        "allow_pet": True,
        "allow_events": True,
        "has_piped_gas": True,
        "status": "ACTIVE",
        "type": "HOUSE",
        "id_user": user.id_user,
        "address": {
            "street": "R. Antônio Joaquim Pequeno",
            "city": "Campina Grande",
            "number": "595",
            "complement": "",
            "zip_code": "58429105",
        },
        "vacancies": [
            {
                "has_bathroom": True,
                "has_garage": True,
                "has_furniture": True,
                "has_cable_internet": True,
                "is_shared_room": False,
                "allowed_smoker": False,
                "required_organized_person": True,
                "required_extroverted_person": False,
                "gender": "FEMALE",
                "price": 0,
            }
        ],
    }

    client.create(json.dumps(data_anuncio1))
    client.create(json.dumps(data_anuncio2))
    client.create(json.dumps(data_anuncio3))

    filters = {
        "filters": [
            AnnouncementTagsEnum.IS_CLOSE_TO_UNIVERSITY,
            AnnouncementTagsEnum.IS_CLOSE_TO_SUPERMARKET,
            AnnouncementTagsEnum.ALLOW_PETS,
            AnnouncementTagsEnum.FEMALE_GENDER,
        ]
    }

    response = client.list_announcements_by_filter(filters)

    assert response.status_code == 200
    assert list(map(lambda x: x["title"], response.json())) == [
        "anuncio 3",
        "anuncio 1",
        "anuncio 2",
    ]


def test_disable_announcement(announcement, session, client):
    session.add(announcement)
    session.commit()

    client.disable(id=announcement.id_announcement)
    response = client.get_by_id(id=announcement.id_announcement)
    assert response.status_code == 200
    assert response.json()["status"] == "DISABLED"


def test_enable_announcement(announcement, session, client):
    session.add(announcement)
    session.commit()

    client.disable(id=announcement.id_announcement)
    client.enable(id=announcement.id_announcement)
    response = client.get_by_id(id=announcement.id_announcement)
    assert response.status_code == 200
    assert response.json()["status"] == "ACTIVE"
