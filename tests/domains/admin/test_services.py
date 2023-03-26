import pytest

from databases import Database
from passlib.context import CryptContext
from uuid import uuid4

from ecg.domains.admin.exceptions import (
    UserAccessDeniedError,
    UserSelfDeletionError,
    UserNotFoundError,
)
from ecg.domains.admin.services import (
    authenticate_user,
    generate_user,
    hash_password,
    verify_password,
    is_admin,
    create_user,
    delete_user,
    get_user,
)
from ecg.domains.admin.models import User, RoleEnum
from ecg.domains.admin import repositories as repo


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


@pytest.fixture(autouse=True)
def repo_mock(mocker, user_data):
    mock = mocker.Mock(spec=repo)
    mocker.patch("ecg.domains.admin.services.repo", mock)
    mock.get.return_value = User(
        id=user_data["id"],
        email=user_data["email"],
        password=hash_password(user_data["password"]),
        role=user_data["role"],
    )
    return mock


@pytest.mark.asyncio
async def test_authenticate_user_success(db_mock, user_data):
    user_db_data = user_data.copy()
    user_db_data["password"] = hash_password(user_data["password"])

    user = await authenticate_user(user_data["email"], user_data["password"], db_mock)

    assert user.email == user_data["email"]
    assert user.role == user_data["role"]


@pytest.mark.asyncio
async def test_authenticate_user_failure(db_mock, user_data):
    with pytest.raises(UserAccessDeniedError):
        await authenticate_user(user_data["email"], "wrongpassword", db_mock)


def test_generate_user(user_data):
    new_user = generate_user(user_data["email"], user_data["password"])

    assert new_user.email == user_data["email"]
    assert new_user.role == RoleEnum.USER


def test_hash_password():
    password = "test_password"
    hashed_password = hash_password(password)

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    assert pwd_context.verify(password, hashed_password)


def test_verify_password(user_data):
    hashed_password = hash_password(user_data["password"])

    assert verify_password(user_data["password"], hashed_password)


def test_is_admin(user_data):
    user = User(**user_data)

    assert not is_admin(user)

    user.role = RoleEnum.ADMIN
    assert is_admin(user)


@pytest.mark.asyncio
async def test_create_user(db_mock, user_data):
    creator = User(**user_data)
    creator.role = RoleEnum.ADMIN

    user_email = "newuser@example.com"
    user_password = "new_password"

    new_user = await create_user(db_mock, creator, user_email, user_password)

    assert new_user.email == user_email
    assert new_user.role == RoleEnum.USER


@pytest.mark.asyncio
async def test_delete_user_success(db_mock, repo_mock, user_data):
    current_user_data = user_data.copy()
    current_user_data["role"] = RoleEnum.ADMIN
    current_user = User(**current_user_data)

    user_to_delete_data = {
        "id": uuid4(),
        "email": "to_delete@example.com",
        "password": "test_password",
        "role": RoleEnum.USER,
    }

    repo_mock.get.return_value = User(**user_to_delete_data)

    await delete_user(db_mock, current_user, user_to_delete_data["email"])
    repo_mock.delete.assert_called_once_with(db_mock, user_to_delete_data["email"])


@pytest.mark.asyncio
async def test_delete_user_self_deletion(db_mock, repo_mock, user_data):
    current_user_data = user_data.copy()
    current_user_data["role"] = RoleEnum.ADMIN
    current_user = User(**current_user_data)

    repo_mock.get.return_value = current_user

    with pytest.raises(UserSelfDeletionError):
        await delete_user(db_mock, current_user, current_user_data["email"])


@pytest.mark.asyncio
async def test_delete_user_not_found(db_mock, repo_mock, user_data):
    current_user_data = user_data.copy()
    current_user_data["role"] = RoleEnum.ADMIN
    current_user = User(**current_user_data)

    repo_mock.get.return_value = None

    with pytest.raises(UserNotFoundError):
        await delete_user(db_mock, current_user, "notfound@example.com")


@pytest.mark.asyncio
async def test_delete_user_not_admin(db_mock, repo_mock, user_data):
    current_user = User(**user_data)

    repo_mock.get.return_value = None

    with pytest.raises(UserAccessDeniedError):
        await delete_user(db_mock, current_user, "notadmin@example.com")


@pytest.mark.asyncio
async def test_get_user(db_mock, repo_mock, user_data):
    user_email = "newuser@example.com"

    await get_user(db_mock, user_email)

    repo_mock.get.assert_called_once_with(db_mock, user_email)
