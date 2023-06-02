import pytest

from utilities.login_utils import *
from config.config import database

# noinspection SpellCheckingInspection
hashed_password = "$2b$12$4M2FCTLRZ7ZtrqIfaOHx0uFPSQ7czthVwFvmb14NGOGvBmbz95.xO"


def test_get_hash():
    assert "password" not in get_password_hash("password")


def test_verify_password_success():
    assert verify_password("password", hashed_password)


def test_verify_password_failure():
    assert not verify_password("other-string", hashed_password)


def test_get_user_success():
    user = get_user(database, "user1")
    assert user.username == "user1"
    assert user.hashed_password is not None


def test_get_user_failure():
    user = get_user(database, "user2")
    assert user is None


def test_authenticate_user_not_a_user():
    user = authenticate_user(database, "user2", "password")
    assert user is False


def test_authenticate_user_invalid_password():
    user = authenticate_user(database, "user1", "other-string")
    assert user is False


def test_authenticate_user_success():
    user = authenticate_user(database, "user1", "password")
    assert user.username == "user1"


def test_register_user_repeated_username():
    form = UserRegistrationForm(
        username="user1",
        password="password",
    )
    with pytest.raises(HTTPException):
        register_user(form)


def test_register_user_valid_username():
    form = UserRegistrationForm(
        username="user3",
        password="password",
    )
    register_user(form)
    user_hashed_pw = database.users.get("user3")["hashed_password"]
    assert "password" not in user_hashed_pw
    assert user_hashed_pw is not None

