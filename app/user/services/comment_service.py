from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.user.repositories.comment_repository import CommentRepository
from app.user.schemas import CommentCreate, CommentView
from app.user.schemas.comment import CommentUpdate


class CommentService(BaseService[CommentCreate, CommentUpdate, CommentView]):
    def __init__(self, db: Session):
        super().__init__(
            repository=CommentRepository,
            db=db,
        )

    def get_comments_by_id_user(self, id_user: UUID) -> List[CommentView]:
        repository: CommentRepository = self.repository
        return repository.get_comments_by_id_user_commented(id_user_commented=id_user)
