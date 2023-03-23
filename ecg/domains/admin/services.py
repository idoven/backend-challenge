from uuid import uuid4

from databases import Database
from passlib.context import CryptContext

from .exceptions import UserAccessDeniedError, UserNotFoundError, UserSelfDeletionError
from . import repositories as repo
from .models import User, RoleEnum

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hashing password
def hash_password(password: str):
    return pwd_context.hash(password)


# Verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str, db: Database):
    user = await repo.get(db, email)
    if user and verify_password(password, user.password):
        return user
    else:
        raise UserAccessDeniedError


def generate_user(email: str, password: str, admin: bool = False) -> User:
    hashed_password = hash_password(password)
    role = RoleEnum.ADMIN if admin else RoleEnum.USER
    return User(id=uuid4(), email=email, password=hashed_password, role=role)


async def create_user(
    db: Database, creator: User, email: str, password: str, admin: bool = False
) -> User:
    if not is_admin(creator):
        raise UserAccessDeniedError
    user = generate_user(email, password, admin)
    await repo.create(db, user)
    return user


async def delete_user(db: Database, current_user: User, email: str) -> None:
    if not is_admin(current_user):
        raise UserAccessDeniedError

    user = await repo.get(db, email)
    if user is None:
        raise UserNotFoundError

    if current_user.email == user.email:
        raise UserSelfDeletionError

    await repo.delete(db, email)


async def get_user(db: Database, email: str) -> User:
    user = await repo.get(db, email)
    if user is None:
        raise UserNotFoundError

    return user


# Check if user has role admin
def is_admin(user: User) -> bool:
    return user.role == RoleEnum.ADMIN
