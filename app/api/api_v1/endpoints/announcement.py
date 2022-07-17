from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

import app.api.deps as deps
from app.announcement.schemas.announcement import (
    AnnouncementCreateBodyPayload,
    AnnouncementFilter,
    AnnouncementUpdate,
    AnnouncementView,
)
from app.announcement.services.announcement_service import AnnouncementService
from app.common.exceptions import RecordNotFoundException, RecordNotFoundHTTPException

router = APIRouter()


@router.post("/", response_model=AnnouncementView)
def create_announcement(
    announcement_create: AnnouncementCreateBodyPayload,
    service: AnnouncementService = Depends(deps.get_announcement_service),
):
    return service.create(create=announcement_create)


@router.get("/", response_model=List[AnnouncementView])
def get_all_announcement(service: AnnouncementService = Depends(deps.get_announcement_service)):
    return service.get_all()


@router.get("/{id_announcement}", response_model=AnnouncementView)
def get_announcement_by_id(
    id_announcement: UUID, service: AnnouncementService = Depends(deps.get_announcement_service)
):
    try:
        return service.get_by_id(id_announcement=id_announcement)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Announcement not found")


@router.delete("/{id_announcement}")
def delete_announcement(
    id_announcement: UUID, service: AnnouncementService = Depends(deps.get_announcement_service)
):
    try:
        service.delete(id_announcement=id_announcement)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Announcement not found")


@router.put("/{id_announcement}", response_model=AnnouncementView)
def update_announcement(
    announcement_update: AnnouncementUpdate,
    id_announcement: UUID,
    service: AnnouncementService = Depends(deps.get_announcement_service),
):
    return service.update(update=announcement_update, id_announcement=id_announcement)


@router.post("/filter")
def list_announcements_by_filter(announcement_filter: list, service: AnnouncementService = Depends(deps.get_announcement_service)):
    return service.filter(announcement_filter)