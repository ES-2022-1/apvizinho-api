import json
from datetime import datetime

import pytest

from .base_client import BaseClient


class TodoListClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="todo_list")


@pytest.fixture
def todo_list_client(client):
    return TodoListClient(client)


@pytest.fixture
def todo_list(make_todo_list):
    return make_todo_list()


def test_create_todo_list(todo_list_client):
    data = {"nome": "string", "prazo": datetime.now()}
    response = todo_list_client.create(json.dumps(data))

    assert response.status_code == 200
    assert response.json()["nome"] == "string"
