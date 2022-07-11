import json

import pytest

from app.announcement.schemas.vacancy import GenderEnum

from .base_client import BaseClient


class VacancyClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="vacancy")


@pytest.fixture
def client(client):
    return VacancyClient(client)


@pytest.fixture
def vacancy(make_vacancy):
    return make_vacancy()


def test_create_vacancy(client, session, make_announcement):
    announcement = make_announcement()
    session.add(announcement)
    session.commit()

    data = {
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
        "id_announcement": announcement.id_announcement,
    }

    response = client.create(json.dumps(data))

    assert response.status_code == 200


@pytest.mark.parametrize(
    "field,expected_field",
    [
        ("has_bathroom", False),
        ("has_garage", False),
        ("has_furniture", False),
        ("has_cable_internet", False),
        ("is_shared_room", False),
        ("allowed_smoker", False),
        ("required_organized_person", False),
        ("required_extroverted_person", False),
        ("gender", GenderEnum.UNKNOWN),
        ("price", 50),
    ],
)
def test_update_vacancy(vacancy, session, client, field, expected_field):
    session.add(vacancy)
    session.commit()

    data = {field: expected_field}

    response = client.update(id=vacancy.id_vacancy, update=json.dumps(data))
    assert response.status_code == 200
    assert response.json()[field] == expected_field


def test_delete_vacancy(vacancy, session, client):
    session.add(vacancy)
    session.commit()

    client.delete(id=vacancy.id_vacancy)
    response = client.get_by_id(id=vacancy.id_vacancy)
    assert response.status_code == 404
    assert response.json()["detail"] == "Vacancy not found"


def test_get_vacancy_by_id(vacancy, session, client):
    session.add(vacancy)
    session.commit()
    response = client.get_by_id(id=vacancy.id_vacancy)
    assert response.status_code == 200
    assert response.json()["id_vacancy"] == str(vacancy.id_vacancy)


def test_list_vacancys(vacancy, session, client):
    session.add(vacancy)
    session.commit()
    response = client.get_all()

    assert response.status_code == 200
    assert len(response.json()) == 1
