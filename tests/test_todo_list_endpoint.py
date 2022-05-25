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


@pytest.mark.parametrize(
    "field,expected_field",
    [
        ("nome", "novo_nome"),
        ("prazo", "2022-05-25T20:22:46.533000+00:00"),
    ],
)
def test_update_todo_list(todo_list, session, todo_list_client, field, expected_field):
    session.add(todo_list)
    session.commit()

    data = {field: expected_field}

    response = todo_list_client.update(id=todo_list.id_todo_list, update=json.dumps(data))
    assert response.status_code == 200
    assert response.json()[field] == expected_field


def test_delete_todo_item(todo_list, session, todo_list_client):
    session.add(todo_list)
    session.commit()

    todo_list_client.delete(id=todo_list.id_todo_list)
    response = todo_list_client.get_by_id(id=todo_list.id_todo_list)
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo List not found"


def test_get_todo_list_by_id(todo_list, session, todo_list_client):
    session.add(todo_list)
    session.commit()
    response = todo_list_client.get_by_id(id=todo_list.id_todo_list)

    assert response.status_code == 200
    assert response.json()["nome"] == str(todo_list.nome)
    assert response.json()["id_todo_list"] == str(todo_list.id_todo_list)


def test_list_todo_list(todo_list, session, todo_list_client):
    session.add(todo_list)
    session.commit()
    response = todo_list_client.get_all()

    assert response.status_code == 200
    assert len(response.json()) == 1
