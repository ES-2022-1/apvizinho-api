from uuid import UUID

from sqlalchemy.orm import Session

import app.common.models as models
from app.common.repositories.base import BaseRepository


class ReviewRepository(BaseRepository[models.Review, UUID]):
    def __init__(self, db: Session):
        super(ReviewRepository, self).__init__(
            models.Review.id_review,
            model_class=models.Review,
            db=db,
        )
