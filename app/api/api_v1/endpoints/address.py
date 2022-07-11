from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

import app.api.deps as deps
from app.announcement.schemas.address import AddressCreate, AddressUpdate, AddressView
from app.announcement.services.address_service import AddressService
from app.common.exceptions import RecordNotFoundException, RecordNotFoundHTTPException

router = APIRouter()


@router.post("/", response_model=AddressView)
def create_address(
    address_create: AddressCreate, service: AddressService = Depends(deps.get_address_service)
):
    return service.create(create=address_create)


@router.get("/", response_model=List[AddressView])
def get_all_address(service: AddressService = Depends(deps.get_address_service)):
    return service.get_all()


@router.get("/{id_address}", response_model=AddressView)
def get_address_by_id(
    id_address: UUID, service: AddressService = Depends(deps.get_address_service)
):
    try:
        return service.get_by_id(id_address=id_address)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Address not found")


@router.delete("/{id_address}")
def delete_address(id_address: UUID, service: AddressService = Depends(deps.get_address_service)):
    try:
        service.delete(id_address=id_address)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Addres not found")


@router.put("/{id_address}", response_model=AddressView)
def update_address(
    address_update: AddressUpdate,
    id_address: UUID,
    service: AddressService = Depends(deps.get_address_service),
):
    return service.update(update=address_update, id_address=id_address)
