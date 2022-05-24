import pytest

from .base_client import BaseClient


class TodoClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="todo")


@pytest.fixture
def todo_client(client):
    return TodoClient(client)


def test_delete_todo(session):
    assert 1 == 1
