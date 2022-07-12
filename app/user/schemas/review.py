from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.user.schemas.user import UserView


class ReviewBase(BaseModel):
    comment: str
    score: int = Field(ge=0, le=5)


class ReviewBodyPayload(ReviewBase):
    ...


class ReviewCreate(ReviewBase):
    id_user: UUID


class ReviewView(ReviewBase):
    id_review: UUID
    user: UserView

    class Config:
        orm_mode = True


class ReviewUpdate(BaseModel):
    comment: Optional[str]
    score: Optional[int] = Field(ge=0, le=5)
