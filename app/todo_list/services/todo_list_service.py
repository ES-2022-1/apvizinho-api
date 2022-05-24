from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.todo_list.repositories.todo_list_repository import TodoListRepository
from app.todo_list.schemas import TodoListCreate, TodoListUpdate, TodoListView


class TodoListService(BaseService[TodoListCreate, TodoListUpdate, TodoListView]):
    def __init__(self, db: Session):
        super().__init__(
            repository=TodoListRepository,
            db=db,
        )
