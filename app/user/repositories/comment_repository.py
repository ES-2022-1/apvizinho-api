from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

import app.common.models as models
from app.common.models.profile_comment import Profile_Comment
from app.common.repositories.base import BaseFinder, BaseRepository


class CommentsFinder(BaseFinder[models.Profile_Comment]):
    @classmethod
    def get_instance(cls, db: Session):
        return cls(
            (db.query(models.Profile_Comment).filter(models.Profile_Comment.deleted_at.is_(None)))
        )

    def filtered_by_id_user_commented(self, id_user_commented: UUID):
        if id_user_commented:
            return CommentsFinder(
                self.base_query.filter(
                    models.Profile_Comment.id_user_commented == id_user_commented
                )
            )


class CommentRepository(BaseRepository[models.Profile_Comment, UUID]):
    def __init__(self, db: Session):
        super(CommentRepository, self).__init__(
            models.Profile_Comment.id_comment,
            model_class=models.Profile_Comment,
            db=db,
            finder=CommentsFinder,
        )

    def get_comments_by_id_user_commented(self, id_user_commented: UUID) -> List[Profile_Comment]:
        finder: CommentsFinder = self.finder

        return finder.filtered_by_id_user_commented(id_user_commented=id_user_commented).all()
