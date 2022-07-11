from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

import app.api.deps as deps
from app.common.exceptions import RecordNotFoundException, RecordNotFoundHTTPException
from app.local.schemas.room import RoomCreate, RoomUpdate, RoomView
from app.local.services.room_service import RoomService

router = APIRouter()


@router.post("/", response_model=RoomView)
def create_room(room_create: RoomCreate, service: RoomService = Depends(deps.get_room_service)):
    return service.create(create=room_create)


@router.get("/", response_model=List[RoomView])
def get_all_room(service: RoomService = Depends(deps.get_room_service)):
    return service.get_all()


@router.get("/{id_room}", response_model=RoomView)
def get_room_by_id(id_room: UUID, service: RoomService = Depends(deps.get_room_service)):
    try:
        return service.get_by_id(id_room=id_room)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Room not found")


@router.delete("/{id_room}")
def delete_room(id_room: UUID, service: RoomService = Depends(deps.get_room_service)):
    try:
        service.delete(id_room=id_room)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Room not found")


@router.put("/{id_room}", response_model=RoomView)
def update_room(
    room_update: RoomUpdate,
    id_room: UUID,
    service: RoomService = Depends(deps.get_room_service),
):
    return service.update(update=room_update, id_room=id_room)
