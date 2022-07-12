from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.user.repositories.review_repository import ReviewRepository
from app.user.schemas import ReviewCreate, ReviewView
from app.user.schemas.review import ReviewUpdate


class ReviewService(BaseService[ReviewCreate, ReviewUpdate, ReviewView]):
    def __init__(self, db: Session):
        super().__init__(
            repository=ReviewRepository,
            db=db,
        )
