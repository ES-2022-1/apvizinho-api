import json

import pytest

from .base_client import BaseClient


class UserClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="user")

    def review(self, id_user, data):
        return self.client.post(f"/{self.path}/{id_user}/review", data=data, headers=self.headers)

    def comment(self, data):
        return self.client.post(
            f"/{self.path}/comment",
            data=data,
            headers=self.headers,
        )

    def get_comments_by_id_user_commented(self, id_user_commented):
        return self.client.get(
            f"/{self.path}/{id_user_commented}/comments",
            headers=self.headers,
        )

    def get_announcements_by_id_user(self, id_user):
        return self.client.get(
            f"/{self.path}/{id_user}/announcements",
            headers=self.headers,
        )


@pytest.fixture
def user_client(client):
    return UserClient(client)


@pytest.fixture
def announcement(make_announcement):
    return make_announcement()


@pytest.fixture
def user(make_user):
    return make_user()


@pytest.fixture
def comment(make_comment):
    return make_comment()


@pytest.fixture
def user2(make_user):
    return make_user()


@pytest.fixture
def review(make_review):
    return make_review()


def test_create_user(user_client):
    data = {
        "firstname": "Nome",
        "surname": "Sobrenome",
        "email": "email@email.com.br",
        "cellphone": "99999999999",
        "document": "99999999999",
        "birthdate": "2022-07-10",
        "password": "SEGREDO!",
    }

    response = user_client.create(json.dumps(data))

    assert response.status_code == 200
    assert response.json()["firstname"] == "Nome"


@pytest.mark.parametrize(
    "field,expected_field",
    [
        ("firstname", "Novo Nome"),
        ("surname", "Novo Sobrenome"),
        ("email", "novoemail@email.com.br"),
        ("cellphone", "88888888888"),
        ("document", "88888888888"),
        ("birthdate", "2022-08-10"),
    ],
)
def test_update_user(user, session, user_client, field, expected_field):
    session.add(user)
    session.commit()

    data = {field: expected_field}

    response = user_client.update(id=user.id_user, update=json.dumps(data))
    assert response.status_code == 200
    assert response.json()[field] == expected_field


def test_delete_user(user, session, user_client):
    session.add(user)
    session.commit()

    user_client.delete(id=user.id_user)
    response = user_client.get_by_id(id=user.id_user)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_user_by_id(user, session, user_client):
    session.add(user)
    session.commit()
    response = user_client.get_by_id(id=user.id_user)
    assert response.status_code == 200
    assert response.json()["id_user"] == str(user.id_user)


def test_list_users(user, session, user_client):
    session.add(user)
    session.commit()
    response = user_client.get_all()

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_review(user, session, user_client):
    session.add(user)
    session.commit()

    data = {"comment": "string", "score": 5}
    response = user_client.review(user.id_user, json.dumps(data))
    assert response.status_code == 200
    assert response.json()["user"]["already_reviewed"] == True  # noqa: E712


def test_user_already_reviewed(make_user, session, user_client):
    user = make_user(already_reviewed=True)
    session.add(user)
    session.commit()

    data = {"comment": "string", "score": 5}
    response = user_client.review(user.id_user, json.dumps(data))
    assert response.status_code == 400
    assert response.json()["detail"] == "User Already Reviewd the system"


def test_comment(user, user2, session, user_client):
    session.add(user)
    session.add(user2)
    session.commit()

    data = {
        "comment": "não façam acordo ele é tiktoker",
        "id_user_commented": user.id_user,
        "id_user_writer": user2.id_user,
    }
    response = user_client.comment(json.dumps(data))
    assert response.status_code == 200
    assert response.json()["comment"] == "não façam acordo ele é tiktoker"


def test_get_comments_by_id_user_commented(comment, session, user_client):
    session.add(comment)
    session.commit()

    response = user_client.get_comments_by_id_user_commented(
        id_user_commented=comment.id_user_commented
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert (response.json())[0]["id_user_commented"] == str(comment.id_user_commented)


def test_get_user_announcements(announcement, session, user_client):
    session.add(announcement)
    session.commit()

    response = user_client.get_announcements_by_id_user(id_user=announcement.id_user)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert (response.json())[0]["id_user"] == str(announcement.id_user)
