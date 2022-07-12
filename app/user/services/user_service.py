from uuid import UUID

from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.common.utils import password as password_utils
from app.user.exceptions import UserAlreadyReviewedException
from app.user.repositories.user_repository import UserRepository
from app.user.schemas import UserCreate, UserUpdate, UserView
from app.user.schemas.review import ReviewBodyPayload, ReviewCreate, ReviewView
from app.user.schemas.user import UserCreateHashedPassword
from app.user.services.review_service import ReviewService


class UserService(BaseService[UserCreate, UserUpdate, UserView]):
    def __init__(self, db: Session, review_service: ReviewService):
        super().__init__(
            repository=UserRepository,
            db=db,
        )

        self.review_service = review_service

    def create(self, create: UserCreate) -> UserView:
        user_create = UserCreateHashedPassword(
            **create.dict(), password_hash=password_utils.create_hash(create.password)
        )

        return self.repository.add(user_create)

    def review(self, id_user: UUID, review_body_payload: ReviewBodyPayload) -> ReviewView:
        user = self.get_by_id(id_user=id_user)

        if user.already_reviewed:
            raise UserAlreadyReviewedException

        review_create = ReviewCreate(**review_body_payload.dict(), id_user=id_user)
        user_update = UserUpdate(already_reviewed=True)
        self.update(id_user=id_user, update=user_update)
        return self.review_service.create(review_create)
