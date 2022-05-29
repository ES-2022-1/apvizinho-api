import json

import pytest

from .base_client import BaseClient


class TodoItemClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="todo_item")


@pytest.fixture
def client(client):
    return TodoItemClient(client)


@pytest.fixture
def todo_item(make_todo_item):
    return make_todo_item()


@pytest.fixture
def todo_list(make_todo_list):
    return make_todo_list()


def test_create_todo_item(client, session, todo_list):
    session.add(todo_list)
    session.commit()

    data = {"nome": "string", "description": "string", "id_todo_list": todo_list.id_todo_list}
    response = client.create(json.dumps(data))

    assert response.status_code == 200
    assert response.json()["nome"] == "string"
    assert response.json()["description"] == "string"
    assert response.json()["id_todo_list"] == str(todo_list.id_todo_list)


@pytest.mark.parametrize(
    "field,expected_field",
    [
        ("nome", "novo_nome"),
        ("description", "nova_description"),
    ],
)
def test_update_todo_item(todo_item, session, client, field, expected_field):
    session.add(todo_item)
    session.commit()

    data = {field: expected_field}

    response = client.update(id=todo_item.id_todo_item, update=json.dumps(data))
    assert response.status_code == 200
    assert response.json()[field] == expected_field


def test_delete_todo_item(todo_item, session, client):
    session.add(todo_item)
    session.commit()

    client.delete(id=todo_item.id_todo_item)
    response = client.get_by_id(id=todo_item.id_todo_item)
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo Item not found"


def test_get_todo_item_by_id(todo_item, session, client):
    session.add(todo_item)
    session.commit()
    response = client.get_by_id(id=todo_item.id_todo_item)

    assert response.status_code == 200
    assert response.json()["nome"] == str(todo_item.nome)
    assert response.json()["id_todo_item"] == str(todo_item.id_todo_item)


def test_list_todo_item(todo_item, session, client):
    session.add(todo_item)
    session.commit()
    response = client.get_all()

    assert response.status_code == 200
    assert len(response.json()) == 1
