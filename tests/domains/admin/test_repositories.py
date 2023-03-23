import pytest
from asyncpg import UniqueViolationError
from databases import Database
from uuid import uuid4

from ecg.domains.admin.repositories import (
    create,
    get,
    delete
)
from ecg.sql.admin import CREATE_USER_QUERY, \
    GET_USER_QUERY, DELETE_USER_QUERY
from ecg.domains.admin.models import User, RoleEnum
from ecg.domains.admin.exceptions import NotUniqueUserError


@pytest.fixture
def user_data():
    return {
        "id": uuid4(),
        "email": "test@example.com",
        "password": "test_password",
        "role": RoleEnum.USER,
    }


@pytest.fixture
def db_mock(mocker):
    return mocker.Mock(spec=Database)


@pytest.mark.asyncio
async def test_create(db_mock, user_data):
    user = User(**user_data)
    db_mock.fetch_one.return_value = user_data

    result = await create(db_mock, user)

    db_mock.fetch_one.assert_called_once_with(CREATE_USER_QUERY, user.dict())
    assert result == user


@pytest.mark.asyncio
async def test_create_user_unique_violation(db_mock, user_data):
    user = User(**user_data)
    db_mock.fetch_one.side_effect = UniqueViolationError(None, None, None)

    with pytest.raises(NotUniqueUserError):
        await create(db_mock, user)

    db_mock.fetch_one.assert_called_once_with(CREATE_USER_QUERY, user.dict())


@pytest.mark.asyncio
async def test_get(db_mock, user_data):
    user = User(**user_data)
    db_mock.fetch_one.return_value = user_data

    result = await get(db_mock, user.email)

    db_mock.fetch_one.assert_called_once_with(GET_USER_QUERY, {"email": user.email})
    assert result == user


@pytest.mark.asyncio
async def test_get_not_found(db_mock, user_data):
    db_mock.fetch_one.return_value = None

    result = await get(db_mock, user_data["email"])

    db_mock.fetch_one.assert_called_once_with(
        GET_USER_QUERY,
        {"email": user_data["email"]}
    )
    assert result is None


@pytest.mark.asyncio
async def test_delete_user(db_mock, user_data):
    await delete(db_mock, user_data["email"])

    db_mock.execute.assert_called_once_with(DELETE_USER_QUERY,
                                            {"email": user_data["email"]})
