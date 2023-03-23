from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(BaseModel):
    id: UUID
    email: str
    password: str
    role: RoleEnum = RoleEnum.USER
