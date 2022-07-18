from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CommentBase(BaseModel):
    comment: str
    id_user_commented: UUID
    id_user_writer: UUID


class CommentBodyPayload(CommentBase):
    ...


class CommentCreate(CommentBase):
    ...


class CommentView(CommentBase):
    id_comment: UUID

    class Config:
        orm_mode = True


class CommentUpdate(BaseModel):
    comment: Optional[str]
