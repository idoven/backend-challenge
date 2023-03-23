from asyncpg import UniqueViolationError
from databases import Database

from .exceptions import NotUniqueUserError
from .models import User
from ecg.sql.admin import CREATE_USER_QUERY, GET_USER_QUERY, DELETE_USER_QUERY


async def create(db: Database, user: User) -> User:
    values = user.dict()
    try:
        user_row = await db.fetch_one(CREATE_USER_QUERY, values)
    except UniqueViolationError:
        raise NotUniqueUserError
    return User(**user_row)


async def get(db: Database, email: str) -> User | None:
    user_row = await db.fetch_one(GET_USER_QUERY, {"email": email})
    if user_row:
        return User(**user_row)
    return None


async def delete(db: Database, email: str) -> None:
    await db.execute(DELETE_USER_QUERY, {"email": email})
