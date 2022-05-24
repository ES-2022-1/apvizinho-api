from uuid import UUID

from sqlalchemy.orm import Session

import app.common.models as models
from app.common.repositories.base import BaseRepository


class TodoListRepository(BaseRepository[models.TodoList, UUID]):
    def __init__(self, db: Session):
        super(TodoListRepository, self).__init__(
            models.TodoList.id_todo_list,
            model_class=models.TodoList,
            db=db,
        )
