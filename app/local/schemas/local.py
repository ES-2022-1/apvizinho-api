from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.local.schemas.room import RoomView


class LocalBase(BaseModel):
    title: str
    description: str
    is_close_to_university: bool
    is_close_to_supermarket: bool
    has_furniture: bool
    has_internet: bool
    allow_pet: bool
    allow_events: bool
    has_piped_gas: bool
    type: str
    status: str

class LocalCreate(LocalBase):
    ...


class LocalView(LocalBase):
    id_local: UUID
    id_user: UUID
    id_address: UUID
    rooms: List[RoomView]

    class Config:
        orm_mode = True


class LocalUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    is_close_to_university: Optional[bool]
    is_close_to_supermarket: Optional[bool]
    has_furniture: Optional[bool]
    has_internet: Optional[bool]
    allow_pet: Optional[bool]
    allow_events: Optional[bool]
    has_piped_gas: Optional[bool]
    type: Optional[bool]
    status: Optional[bool]