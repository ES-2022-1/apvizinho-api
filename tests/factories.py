import uuid
from datetime import datetime

import pytest

from app.common import models


@pytest.fixture
def make_todo_list():
    defaults = dict(nome="Lista de Compra", prazo=datetime.now())

    def _make_todo_list(**overrides):
        return models.TodoList(id_todo_list=uuid.uuid4(), **{**defaults, **overrides})

    return _make_todo_list


@pytest.fixture
def make_todo_item(make_todo_list):
    defaults = dict(
        nome="Item 1", description="Item numero 1 da lista de compras", todo_list=make_todo_list()
    )

    def _make_todo_item(**overrides):
        return models.TodoItem(id_todo_item=uuid.uuid4(), **{**defaults, **overrides})

    return _make_todo_item
