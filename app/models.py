from pydantic import SecretStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__: str = "users"  # type: ignore[misc]

    id: int | None = Field(default=None, primary_key=True)
    username: str
    password_hash: str
    name: str


class UserPublic(SQLModel):
    id: int
    username: str
    name: str


class UserCreate(SQLModel):
    username: str
    name: str
    password: SecretStr
