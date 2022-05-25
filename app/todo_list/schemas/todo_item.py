from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TodoItemBase(BaseModel):
    nome: str
    description: str


class TodoItemCreate(TodoItemBase):
    id_todo_list: UUID


class TodoItemView(TodoItemBase):
    id_todo_item: UUID

    class Config:
        orm_mode = True


class TodoItemUpdate(BaseModel):
    nome: Optional[str]
    description: Optional[str]
