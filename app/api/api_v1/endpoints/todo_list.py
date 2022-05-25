from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

import app.api.deps as deps
from app.common.exceptions import RecordNotFoundException, RecordNotFoundHTTPException
from app.todo_list.schemas.todo_list import TodoListCreate, TodoListUpdate, TodoListView
from app.todo_list.services.todo_list_service import TodoListService

router = APIRouter()


@router.post("/", response_model=TodoListView)
def create_todo_list(
    todo_list_create: TodoListCreate, service: TodoListService = Depends(deps.get_todo_list_service)
):
    return service.create(create=todo_list_create)


@router.get("/", response_model=List[TodoListView])
def get_all_todo_list(service: TodoListService = Depends(deps.get_todo_list_service)):
    return service.get_all()


@router.get("/{id_todo_list}", response_model=TodoListView)
def get_todo_list_by_id(
    id_todo_list: UUID, service: TodoListService = Depends(deps.get_todo_list_service)
):
    return service.get_by_id(id_todo_list=id_todo_list)


@router.delete("/{id_todo_list}")
def delete_todo_list(
    id_todo_list: UUID, service: TodoListService = Depends(deps.get_todo_list_service)
):
    try:
        service.delete(id_todo_list=id_todo_list)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Todo List not found")


@router.put("/{id_todo_list}", response_model=TodoListView)
def update_todo_list(
    todo_list_update: TodoListUpdate,
    id_todo_list: UUID,
    service: TodoListService = Depends(deps.get_todo_list_service),
):
    return service.update(update=todo_list_update, id_todo_list=id_todo_list)
