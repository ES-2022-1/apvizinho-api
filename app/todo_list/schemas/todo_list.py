from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.todo_list.schemas import TodoItemView


class TodoListBase(BaseModel):
    nome: str
    prazo: datetime


class TodoListCreate(TodoListBase):
    ...


class TodoListView(TodoListBase):
    id_todo_list: UUID
    items: List[TodoItemView]

    class Config:
        orm_mode = True


class TodoListUpdate(BaseModel):
    nome: Optional[str]
    prazo: Optional[datetime]
