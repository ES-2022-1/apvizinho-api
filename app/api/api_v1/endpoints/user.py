from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

import app.api.deps as deps
from app.common.exceptions import RecordNotFoundException, RecordNotFoundHTTPException
from app.user.schemas import ReviewView, UserCreate, UserUpdate, UserView
from app.user.schemas.review import ReviewBodyPayload
from app.user.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserView)
def create_user(user_create: UserCreate, service: UserService = Depends(deps.get_user_service)):
    return service.create(create=user_create)


@router.get("/", response_model=List[UserView])
def get_all_users(service: UserService = Depends(deps.get_user_service)):
    return service.get_all()


@router.get("/{id_user}", response_model=UserView)
def get_users_by_id(id_user: UUID, service: UserService = Depends(deps.get_user_service)):
    try:
        return service.get_by_id(id_user=id_user)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="User not found")


@router.delete("/{id_user}")
def delete_user(id_user: UUID, service: UserService = Depends(deps.get_user_service)):
    try:
        service.delete(id_user=id_user)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="User not found")


@router.put("/{id_user}", response_model=UserView)
def update_user(
    user_update: UserUpdate,
    id_user: UUID,
    service: UserService = Depends(deps.get_user_service),
):
    return service.update(update=user_update, id_user=id_user)


@router.post("/{id_user}/review", response_model=ReviewView)
def review_system(
    review_create: ReviewBodyPayload,
    id_user: UUID,
    service: UserService = Depends(deps.get_user_service),
):
    return service.review(id_user=id_user, review_body_payload=review_create)
