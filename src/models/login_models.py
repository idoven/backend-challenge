from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserRegistrationForm(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    organization: str | None = None
    is_admin: bool = False
    password: str


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    organization: str | None = None
    is_admin: bool = False


class UserInDB(User):
    hashed_password: str
