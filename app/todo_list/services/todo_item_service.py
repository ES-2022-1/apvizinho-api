from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.todo_list.repositories.todo_item_repository import TodoItemRepository
from app.todo_list.schemas.todo_item import TodoItemCreate, TodoItemUpdate, TodoItemView


class TodoItemService(BaseService[TodoItemCreate, TodoItemUpdate, TodoItemView]):
    def __init__(self, db: Session):
        super().__init__(
            repository=TodoItemRepository,
            db=db,
        )
