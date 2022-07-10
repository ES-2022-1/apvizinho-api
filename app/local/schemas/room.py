from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class RoomBase(BaseModel):
    has_bathroom: bool
    has_garage: bool
    has_furniture: bool
    has_cable_internet: bool
    is_shared_room: bool 
    allowed_smoker: bool 
    required_organized_person: bool
    required_ectroverted_person: bool
    gender: str
    price: float 

class RoomCreate(RoomBase):
    id_local: UUID

class RoomView(RoomBase):
    id_room: UUID
    id_local: UUID

    class Config:
        orm_mode = True

class RoomUpdate(BaseModel):
    has_bathroom: Optional[bool]
    has_garage: Optional[bool]
    has_furniture: Optional[bool]
    has_cable_internet: Optional[bool]
    is_shared_room: Optional[bool]
    allowed_smoker: Optional[bool] 
    required_organized_person: Optional[bool]
    required_ectroverted_person: Optional[bool]
    gender: Optional[str]
    price: Optional[float] 