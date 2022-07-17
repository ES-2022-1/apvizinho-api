from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.announcement.schemas.address import AddressCreate, AddressView
from app.announcement.schemas.vacancy import VacancyBase, VacancyView


class StatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"


class AnnouncementTypeEnum(str, Enum):
    HOUSE = "HOUSE"
    APARTMENT = "APARTMENT"


class AnnouncementBase(BaseModel):
    title: str
    description: str
    is_close_to_university: bool
    is_close_to_supermarket: bool
    has_furniture: bool
    has_internet: bool
    allow_pet: bool
    allow_events: bool
    has_piped_gas: bool
    status: StatusEnum = StatusEnum.ACTIVE
    type: AnnouncementTypeEnum


class AnnouncementCreateBodyPayload(AnnouncementBase):
    id_user: UUID
    address: AddressCreate
    vacancies: List[VacancyBase]


class AnnouncementCreate(AnnouncementBase):
    id_address: UUID
    id_user: UUID


class AnnouncementView(AnnouncementBase):
    id_announcement: UUID
    id_user: UUID
    id_address: UUID
    vacancies: List[VacancyView]
    address: AddressView

    class Config:
        orm_mode = True


class AnnouncementUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    is_close_to_university: Optional[bool]
    is_close_to_supermarket: Optional[bool]
    has_furniture: Optional[bool]
    has_internet: Optional[bool]
    allow_pet: Optional[bool]
    allow_events: Optional[bool]
    has_piped_gas: Optional[bool]
    type: Optional[AnnouncementTypeEnum]
    status: Optional[StatusEnum]

class AnnouncementFilter(BaseModel):
    filters: list
