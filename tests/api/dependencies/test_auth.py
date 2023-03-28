import jwt
import pytest
from databases import Database
from fastapi import HTTPException, status

from ecg.api.dependencies.auth import create_access_token, get_current_user
from ecg.config import settings
from ecg.domains.admin.models import RoleEnum, User


# Helper function to generate a user
def generate_user():
    return User(
        id="6d8c2914-3e3a-4d42-8c8e-0f9c1e2e11f1",
        email="test@example.com",
        password="password",
        role=RoleEnum.USER,
    )


@pytest.fixture
def token():
    user = generate_user()
    access_token = create_access_token(data={"sub": user.email})
    return access_token


def test_create_access_token():
    user = generate_user()
    access_token = create_access_token(data={"sub": user.email})
    decoded = jwt.decode(access_token, settings.jwt_key, algorithms=["HS256"])
    assert decoded["sub"] == user.email


@pytest.fixture
def db_mock(mocker):
    return mocker.Mock(spec=Database)


@pytest.mark.asyncio
async def test_get_current_user(mocker, token, db_mock):
    user = generate_user()
    mocker.patch("ecg.domains.admin.services.get_user", return_value=user)

    authenticated_user = await get_current_user(token=token, db=db_mock)

    assert authenticated_user.email == user.email
    assert authenticated_user.role == user.role


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(db_mock):
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token="invalid_token", db=db_mock)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
