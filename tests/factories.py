import uuid

import pytest
from pendulum import date

from app.announcement.schemas.announcement import AnnouncementTypeEnum, StatusEnum
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
def make_address():
    defaults = dict(
        street="string",
        city="string",
        number="string",
        complement="string",
        zip_code="string",
        latitude=20,
        longitude=-20,
    )

    def _make_address(**overrides):
        return models.Address(id_address=uuid.uuid4(), **{**defaults, **overrides})

    return _make_address


@pytest.fixture
def make_announcement(make_user, make_address):
    defaults = dict(
        title="string",
        description="string",
        is_close_to_university=True,
        is_close_to_supermarket=True,
        has_furniture=True,
        has_internet=True,
        allow_pet=True,
        allow_events=True,
        has_piped_gas=True,
        status=StatusEnum.ACTIVE,
        type=AnnouncementTypeEnum.HOUSE,
    )

    def _make_announcement(
        user: models.User = make_user(), address: models.Address = make_address(), **overrides
    ):
        return models.Announcement(
            id_announcement=uuid.uuid4(), user=user, address=address, **{**defaults, **overrides}
        )

    return _make_announcement
