from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

email_field = Field(
    regex="([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+([A-Z|a-z]{2,})+"
)  # noqa: W605

cellphone_field = Field(min_length=11, max_length=11)

document_field = Field(min_length=11, max_length=11)


class UserBase(BaseModel):
    firstname: str
    surname: str
    email: str = email_field
    cellphone: str = cellphone_field
    document: str = document_field
    birthdate: date
    bio: str


class UserCreate(UserBase):
    password: str


class UserCreateHashedPassword(UserBase):
    password_hash: str


class UserView(BaseModel):
    id_user: UUID
    firstname: str
    surname: str
    email: str
    cellphone: str
    birthdate: date
    document: str
    already_reviewed: bool
    bio: Optional[str]
    profile_image: Optional[str]

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    firstname: Optional[str]
    surname: Optional[str]
    email: Optional[str] = email_field
    cellphone: Optional[str] = cellphone_field
    birthdate: Optional[date]
    document: Optional[str] = document_field
    already_reviewed: Optional[bool]
    bio: Optional[str]
    profile_image: Optional[str]
