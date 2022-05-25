import json
from datetime import datetime

import pytest

from .base_client import BaseClient


class TodoClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="todo_list")


@pytest.fixture
def todo_client(client):
    return TodoClient(client)


@pytest.fixture
def todo(make_todo):
    return make_todo()


def test_create_todo(todo_client):
    data = {"nome": "string", "prazo": datetime.now()}
    response = todo_client.create(json.dumps(data))

    assert response.status_code == 200
    assert response.json()["nome"] == "string"
