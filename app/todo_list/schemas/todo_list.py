from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TodoListBase(BaseModel):
    nome: str
    prazo: datetime


class TodoListCreate(TodoListBase):
    ...


class TodoListView(TodoListBase):
    id_todo_list: UUID

    class Config:
        orm_mode = True


class TodoListUpdate(BaseModel):
    nome: Optional[str]
    prazo: Optional[datetime]
