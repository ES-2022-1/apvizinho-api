from uuid import UUID

from sqlalchemy.orm import Session

import app.common.models as models
from app.common.repositories.base import BaseRepository


class TodoItemRepository(BaseRepository[models.TodoItem, UUID]):
    def __init__(self, db: Session):
        super(TodoItemRepository, self).__init__(
            models.TodoItem.id_todo_item,
            model_class=models.TodoItem,
            db=db,
        )
