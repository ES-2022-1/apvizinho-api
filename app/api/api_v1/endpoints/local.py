from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

import app.api.deps as deps
from app.common.exceptions import RecordNotFoundException, RecordNotFoundHTTPException
from app.local.schemas.local import LocalCreateBodyPayload, LocalUpdate, LocalView
from app.local.services.local_service import LocalService

router = APIRouter()


@router.post("/", response_model=LocalView)
def create_local(
    local_create: LocalCreateBodyPayload, service: LocalService = Depends(deps.get_local_service)
):
    return service.create(create=local_create)


@router.get("/", response_model=List[LocalView])
def get_all_local(service: LocalService = Depends(deps.get_local_service)):
    return service.get_all()


@router.get("/{id_local}", response_model=LocalView)
def get_local_by_id(id_local: UUID, service: LocalService = Depends(deps.get_local_service)):
    try:
        return service.get_by_id(id_local=id_local)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Local not found")


@router.delete("/{id_local}")
def delete_local(id_local: UUID, service: LocalService = Depends(deps.get_local_service)):
    try:
        service.delete(id_local=id_local)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Local not found")


@router.put("/{id_local}", response_model=LocalView)
def update_local(
    local_update: LocalUpdate,
    id_local: UUID,
    service: LocalService = Depends(deps.get_local_service),
):
    return service.update(update=local_update, id_local=id_local)
