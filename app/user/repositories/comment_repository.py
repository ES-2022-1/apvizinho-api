from uuid import UUID

from sqlalchemy.orm import Session

import app.common.models as models
from app.common.repositories.base import BaseRepository


class CommentRepository(BaseRepository[models.Profile_Comment, UUID]):
    def __init__(self, db: Session):
        super(CommentRepository, self).__init__(
            models.Profile_Comment.id_comment,
            model_class=models.Profile_Comment,
            db=db,
        )
