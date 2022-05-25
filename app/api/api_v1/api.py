from fastapi import APIRouter

from .endpoints import todo_item, todo_list

api_router = APIRouter()

api_router.include_router(todo_list.router, prefix="/todo_list", tags=["todo_list"])
api_router.include_router(todo_item.router, prefix="/todo_item", tags=["todo_item"])
