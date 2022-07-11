import uuid

import pytest
from pendulum import date

from app.common import models


@pytest.fixture
def make_user():
    defaults = dict(
        email="email@email.com",
        firstname="Nome",
        surname="Sobrenome",
        password_hash="hash",
        cellphone="99999999999",
        document="12345678900",
        birthdate=date(year=2022, month=4, day=3),
    )

    def _make_user(**overrides):
        return models.User(id_user=uuid.uuid4(), **{**defaults, **overrides})

    return _make_user


@pytest.fixture
def make_local(make_address):
    defaults = dict(
        title="Casa Maravilhosa",
        description="Casa espaçosa próxima à UFCG",
        is_close_to_university=True,
        is_close_to_supermarket=True,
        has_furniture=True,
        has_internet=True,
        allow_pet=True,
        allow_events=True,
        has_piped_gas=True,
        type="HOUSE",
        status="ACTIVE",
    )

    def _make_local(address: models.Address = make_address(), **overrides):
        return models.Local(id_local=uuid.uuid4(), address=address ** {**defaults, **overrides})

    return _make_local


@pytest.fixture
def make_room(make_local):
    defaults = dict(
        has_bathroom=True,
        has_garage=True,
        has_furniture=True,
        has_cable_internet=True,
        is_shared_room=True,
        allowed_smoker=True,
        required_organized_person=True,
        required_extroverted_person=True,
        gender="FEMALE",
        price=20,
    )

    def _make_room(local: models.Local = make_local(), **overrides):
        return models.Room(
            id_room=uuid.uuid4(), id_local=local.id_local ** {**defaults, **overrides}
        )

    return _make_room


@pytest.fixture
def make_address():
    defaults = dict(
        street="Avenida Marechal Floriano Peixoto",
        city="Campina Grande",
        number="5255",
        complement="Lote B06",
        zip_code="58434500",
        latitude=20,
        longitude=20,
    )

    def _make_address(**overrides):
        return models.Address(id_address=uuid.uuid4(), **{**defaults, **overrides})

    return _make_address
