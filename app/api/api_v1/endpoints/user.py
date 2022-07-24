from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile

import app.api.deps as deps
from app.announcement.schemas.announcement import AnnouncementView
from app.announcement.services.announcement_service import AnnouncementService
from app.common.exceptions import (
    AWSConfigException,
    AWSConfigExceptionHTTPException,
    RecordNotFoundException,
    RecordNotFoundHTTPException,
)
from app.user.exceptions import UserAlreadyReviewedException, UserAlreadyReviewedHTTPException
from app.user.schemas import ReviewView, UserCreate, UserUpdate, UserView
from app.user.schemas.comment import CommentCreate, CommentView
from app.user.schemas.review import ReviewBodyPayload
from app.user.services.comment_service import CommentService
from app.user.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserView)
def create_user(user_create: UserCreate, service: UserService = Depends(deps.get_user_service)):
    return service.create(create=user_create)


@router.get(
    "/",
    response_model=List[UserView],
    dependencies=[Depends(deps.hass_access)],
)
def get_all_users(service: UserService = Depends(deps.get_user_service)):
    return service.get_all()


@router.get(
    "/{id_user}",
    response_model=UserView,
    dependencies=[Depends(deps.hass_access)],
)
def get_users_by_id(
    id_user: UUID,
    service: UserService = Depends(deps.get_user_service),
):
    try:
        return service.get_by_id(id_user=id_user)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="User not found")


@router.delete(
    "/{id_user}",
    dependencies=[Depends(deps.hass_access)],
)
def delete_user(id_user: UUID, service: UserService = Depends(deps.get_user_service)):
    try:
        service.delete(id_user=id_user)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="User not found")


@router.put(
    "/{id_user}",
    response_model=UserView,
    dependencies=[Depends(deps.hass_access)],
)
def update_user(
    user_update: UserUpdate,
    id_user: UUID,
    service: UserService = Depends(deps.get_user_service),
):
    return service.update(update=user_update, id_user=id_user)


@router.post(
    "/{id_user}/review",
    response_model=ReviewView,
    dependencies=[Depends(deps.hass_access)],
)
def review_system(
    review_create: ReviewBodyPayload,
    id_user: UUID,
    service: UserService = Depends(deps.get_user_service),
):
    try:
        return service.review(id_user=id_user, review_body_payload=review_create)
    except UserAlreadyReviewedException:
        raise UserAlreadyReviewedHTTPException


@router.post(
    "/{id_user}/upload",
    response_model=UserView,
    dependencies=[Depends(deps.hass_access)],
)
def upload_profile_image(
    id_user: UUID,
    file: UploadFile = File(...),
    service: UserService = Depends(deps.get_user_service),
):
    try:
        return service.save_file(id_user=id_user, uploaded_file=file)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="User not found")
    except AWSConfigException as e:
        raise AWSConfigExceptionHTTPException(detail=e.detail)


@router.post(
    "/comment",
    response_model=CommentView,
    dependencies=[Depends(deps.hass_access)],
)
def comment(
    comment_create: CommentCreate,
    service: CommentService = Depends(deps.get_comment_service),
):
    return service.create(create=comment_create)


@router.get(
    "/{id_user}/comments",
    response_model=List[CommentView],
    dependencies=[Depends(deps.hass_access)],
)
def get_user_comments(id_user: UUID, service: CommentService = Depends(deps.get_comment_service)):
    return service.get_comments_by_id_user(id_user=id_user)


@router.get(
    "/{id_user}/announcements",
    response_model=List[AnnouncementView],
    dependencies=[Depends(deps.hass_access)],
)
def get_announcements_by_id_user(
    id_user: UUID, service: AnnouncementService = Depends(deps.get_announcement_service)
):
    return service.get_announcements_by_id_user(id_user=id_user)
