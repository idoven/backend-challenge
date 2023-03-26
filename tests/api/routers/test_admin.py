import pytest
from fastapi import status

from ecg.api.dependencies.auth import create_access_token


def create_test_token(user):
    token = create_access_token({"sub": user.email})
    return token


@pytest.fixture
def test_user_payload():
    return {
        "email": "test_user_payload@test.com",
        "password": "password",
    }


def test_add_user(test_client, test_admin, test_user_payload):
    token = create_test_token(test_admin)
    response = test_client.post(
        "/admin/users",
        json=test_user_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "User added"}


def test_add_user_no_admin(test_client, test_user, test_user_payload):
    token = create_test_token(test_user)
    response = test_client.post(
        "/admin/users",
        json=test_user_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_user(test_client, test_admin, test_user):
    token = create_test_token(test_admin)
    response = test_client.delete(
        f"/admin/users/{test_user.email}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "User deleted"}


def test_delete_user_no_admin(test_client, test_user):
    token = create_test_token(test_user)
    response = test_client.delete(
        f"/admin/users/{test_user.email}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
