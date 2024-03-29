from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile

import app.api.deps as deps
from app.announcement.schemas.announcement import (
    AnnouncementCreateBodyPayload,
    AnnouncementFilter,
    AnnouncementStatus,
    AnnouncementUpdate,
    AnnouncementView,
)
from app.announcement.services.announcement_service import AnnouncementService
from app.common.exceptions import (
    AWSConfigException,
    AWSConfigExceptionHTTPException,
    RecordNotFoundException,
    RecordNotFoundHTTPException,
)

PROTECTED = [Depends(deps.hass_access)]
router = APIRouter(dependencies=PROTECTED)


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


@router.post("/filter", response_model=List[AnnouncementView])
def list_announcements_by_filter(
    announcement_filter: AnnouncementFilter,
    service: AnnouncementService = Depends(deps.get_announcement_service),
):
    return service.filter(announcement_filter)


@router.post("/{id_announcement}/upload")
def upload_announcement_images(
    id_announcement: UUID,
    files: List[UploadFile] = File(...),
    service: AnnouncementService = Depends(deps.get_announcement_service),
):
    try:
        return service.save_multiple_files(id_announcement=id_announcement, uploaded_files=files)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Announcement not found")
    except AWSConfigException as e:
        raise AWSConfigExceptionHTTPException(detail=e.detail)


@router.get("/{id_announcement}/images")
def get_announcement_images(
    id_announcement: UUID,
    service: AnnouncementService = Depends(deps.get_announcement_service),
):
    try:
        return service.get_files(id_announcement=id_announcement)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Announcement not found")


@router.delete("/{id_announcement}/images/{file_name}")
def delete_announcement_image(
    id_announcement: UUID,
    file_name: str,
    service: AnnouncementService = Depends(deps.get_announcement_service),
):
    try:
        return service.delete_file(id_announcement=id_announcement, file_name=file_name)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Announcement not found")
    except AWSConfigException as e:
        raise AWSConfigExceptionHTTPException(detail=e.detail)


@router.patch("/{id_announcement}/disable", response_model=AnnouncementView)
def disable(
    id_announcement: UUID,
    service: AnnouncementService = Depends(deps.get_announcement_service),
):
    announcement_update = AnnouncementUpdate(status=AnnouncementStatus.DISABLED)
    return service.update(update=announcement_update, id_announcement=id_announcement)


@router.patch("/{id_announcement}/enable", response_model=AnnouncementView)
def enable(
    id_announcement: UUID,
    service: AnnouncementService = Depends(deps.get_announcement_service),
):
    announcement_update = AnnouncementUpdate(status=AnnouncementStatus.ACTIVE)
    return service.update(update=announcement_update, id_announcement=id_announcement)
