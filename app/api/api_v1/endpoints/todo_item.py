from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

import app.api.deps as deps
from app.common.exceptions import RecordNotFoundException, RecordNotFoundHTTPException
from app.todo_list.schemas.todo_item import TodoItemCreate, TodoItemUpdate, TodoItemView
from app.todo_list.services.todo_item_service import TodoItemService

router = APIRouter()


@router.post("/", response_model=TodoItemView)
def create_todo_item(
    todo_item_create: TodoItemCreate, service: TodoItemService = Depends(deps.get_todo_item_service)
):
    return service.create(create=todo_item_create)


@router.get("/", response_model=List[TodoItemView])
def get_all_todo_item(service: TodoItemService = Depends(deps.get_todo_item_service)):
    return service.get_all()


@router.get("/{id_todo_item}", response_model=TodoItemView)
def get_todo_item_by_id(
    id_todo_item: UUID, service: TodoItemService = Depends(deps.get_todo_item_service)
):
    try:
        return service.get_by_id(id_todo_item=id_todo_item)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Todo Item not found")


@router.delete("/{id_todo_item}")
def delete_todo_item(
    id_todo_item: UUID, service: TodoItemService = Depends(deps.get_todo_item_service)
):
    try:
        service.delete(id_todo_item=id_todo_item)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Todo Item not found")


@router.put("/{id_todo_item}", response_model=TodoItemView)
def update_todo_item(
    todo_item_update: TodoItemUpdate,
    id_todo_item: UUID,
    service: TodoItemService = Depends(deps.get_todo_item_service),
):
    return service.update(update=todo_item_update, id_todo_item=id_todo_item)
