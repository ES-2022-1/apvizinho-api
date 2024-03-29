from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

import app.api.deps as deps
from app.announcement.schemas.vacancy import (
    VacancyCreate,
    VacancyStatusEnum,
    VacancyUpdate,
    VacancyView,
)
from app.announcement.services.vacancy_service import VacancyService
from app.common.exceptions import RecordNotFoundException, RecordNotFoundHTTPException

PROTECTED = [Depends(deps.hass_access)]
router = APIRouter(dependencies=PROTECTED)


@router.post("/", response_model=VacancyView)
def create_vacancy(
    vacancy_create: VacancyCreate, service: VacancyService = Depends(deps.get_vacancy_service)
):
    return service.create(create=vacancy_create)


@router.get("/", response_model=List[VacancyView])
def get_all_vacancy(service: VacancyService = Depends(deps.get_vacancy_service)):
    return service.get_all()


@router.get("/{id_vacancy}", response_model=VacancyView)
def get_vacancy_by_id(
    id_vacancy: UUID, service: VacancyService = Depends(deps.get_vacancy_service)
):
    try:
        return service.get_by_id(id_vacancy=id_vacancy)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Vacancy not found")


@router.delete("/{id_vacancy}")
def delete_vacancy(id_vacancy: UUID, service: VacancyService = Depends(deps.get_vacancy_service)):
    try:
        service.delete(id_vacancy=id_vacancy)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Vacancy not found")


@router.put("/{id_vacancy}", response_model=VacancyView)
def update_vacancy(
    vacancy_update: VacancyUpdate,
    id_vacancy: UUID,
    service: VacancyService = Depends(deps.get_vacancy_service),
):
    return service.update(update=vacancy_update, id_vacancy=id_vacancy)


@router.patch("/{id_vancancy}/fullfill", response_model=VacancyView)
def fullfill(id_vancancy: UUID, service: VacancyService = Depends(deps.get_vacancy_service)):
    vacancy_update = VacancyUpdate(status=VacancyStatusEnum.FULLFILLED)
    return service.update(update=vacancy_update, id_vacancy=id_vancancy)


@router.patch("/{id_vancancy}/empty", response_model=VacancyView)
def empty(id_vancancy: UUID, service: VacancyService = Depends(deps.get_vacancy_service)):
    vacancy_update = VacancyUpdate(status=VacancyStatusEnum.EMPTY)
    return service.update(update=vacancy_update, id_vacancy=id_vancancy)
