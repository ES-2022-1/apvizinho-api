from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    firstname: str
    surname: str
    email: str
    cellphone: str
    document: str
    birthdate: date


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

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    firstname: Optional[str]
    surname: Optional[str]
    email: Optional[str]
    cellphone: Optional[str]
    birthdate: Optional[date]
    document: Optional[str]
