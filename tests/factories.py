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
def make_local():
    defaults = dict(
        title = "casa bonita",
        description = "casa",
        is_close_to_university = True,
        is_close_to_supermarket = True,
        has_furniture = True,
        has_internet = True,
        allow_pet = True,
        allow_events = True,
        has_piped_gas =  True,
        type =  "casa",
        status = "disponivel"
    )

    def _make_local(**overrides):
        return models.Local(id_local=uuid.uuid4(), **{**defaults, **overrides})

    return _make_local
