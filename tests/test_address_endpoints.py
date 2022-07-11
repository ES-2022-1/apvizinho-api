import json

import pytest

from .base_client import BaseClient


class AddressClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="address")


@pytest.fixture
def client(client):
    return AddressClient(client)


@pytest.fixture
def address(make_address):
    return make_address()


def test_create_address(client):
    data = {
        "street": "Avenida Marechal Floriano Peixoto",
        "city": "Campina Grande",
        "number": "5255",
        "complement": "Lote B06",
        "zip_code": "58434500",
    }

    response = client.create(json.dumps(data))

    assert response.status_code == 200


@pytest.mark.parametrize(
    "field,expected_field",
    [
        ("street", "Rua da Frente"),
        ("city", "Cidade do Lado"),
        ("number", "222"),
        ("complement", "Complementado"),
        ("zip_code", "58434500"),
        ("latitude", 40),
        ("longitude", 20),
    ],
)
def test_update_address(address, session, client, field, expected_field):
    session.add(address)
    session.commit()

    data = {field: expected_field}

    response = client.update(id=address.id_address, update=json.dumps(data))
    assert response.status_code == 200
    assert response.json()[field] == expected_field


def test_delete_address(address, session, client):
    session.add(address)
    session.commit()

    client.delete(id=address.id_address)
    response = client.get_by_id(id=address.id_address)
    assert response.status_code == 404
    assert response.json()["detail"] == "Address not found"


def test_get_address_by_id(address, session, client):
    session.add(address)
    session.commit()
    response = client.get_by_id(id=address.id_address)
    assert response.status_code == 200
    assert response.json()["id_address"] == str(address.id_address)


def test_list_addresss(address, session, client):
    session.add(address)
    session.commit()
    response = client.get_all()

    assert response.status_code == 200
    assert len(response.json()) == 1
