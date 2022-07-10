from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class AddressBase(BaseModel):
    street: str
    city: str
    number: str
    complement: str
    zip_code: str
    latitude: float
    longitude: float


class AddressCreate(AddressBase):
    id_local: UUID


class AddressView(AddressBase):
    id_address: UUID
    id_local: UUID

    class Config:
        orm_mode = True


class AddressUpdate(BaseModel):
    street: Optional[str]
    city: Optional[str]
    number: Optional[str]
    complement: Optional[str]
    zip_code: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
