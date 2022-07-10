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
        address= dict(
            street ='Silva Barbosa',
            city ='Campina Grande',
            number ='975',
            complement ='Próximo a UFCG',
            zip_code ='58400-825'
        ),
        rooms = [
            dict(
                has_bathroom=True, 
                has_garage=True ,
                has_furniture=False,
                has_cable_internet=True,
                is_shared_room=False,
                allowed_smoker=False,
                required_organized_person=True,
                required_extroverted_person=False,
                gender='FEMALE',
                price=500
            )
        ]
    )

    def _make_local(**overrides):
        return models.Local(id_local=uuid.uuid4(), **{**defaults, **overrides})

    return _make_local
