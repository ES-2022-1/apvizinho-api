from datetime import date
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    firstname: str
    surname: str
    email: str
    password: str
    cellphone: str
    document: str
    birthdate: date


class UserCreate(UserBase):
    ...


class UserView(BaseModel):
    firstname: str
    surname: str
    email: str
    cellphone: str
    birthdate: date

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    firstname: Optional[str]
    surname: Optional[str]
    email: Optional[str]
    cellphone: Optional[str]
    birthdate: Optional[date]
