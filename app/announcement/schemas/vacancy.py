from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class GenderEnum(str, Enum):
    FEMALE = "FEMALE"
    MALE = "MALE"
    UNKNOWN = "UNKNOWN"


class VacancyStatusEnum(str, Enum):
    FULLFILLED = "FULLFILLED"
    EMPTY = "EMPTY"


class VacancyBase(BaseModel):
    has_bathroom: bool
    has_garage: bool
    has_furniture: bool
    has_cable_internet: bool
    is_shared_room: bool
    allowed_smoker: bool
    required_organized_person: bool
    required_extroverted_person: bool
    gender: GenderEnum
    price: float


class VacancyCreate(VacancyBase):
    id_announcement: UUID


class VacancyView(VacancyBase):
    id_vacancy: UUID
    id_announcement: UUID

    class Config:
        orm_mode = True


class VacancyUpdate(BaseModel):
    has_bathroom: Optional[bool]
    has_garage: Optional[bool]
    has_furniture: Optional[bool]
    has_cable_internet: Optional[bool]
    is_shared_room: Optional[bool]
    allowed_smoker: Optional[bool]
    required_organized_person: Optional[bool]
    required_extroverted_person: Optional[bool]
    gender: Optional[str]
    price: Optional[float]
    status: Optional[VacancyStatusEnum]
