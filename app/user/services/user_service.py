from typing import List
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.common.exceptions import RecordNotFoundException
from app.common.models import Users
from app.common.repositories.aws_repository import AWSRepository
from app.common.services.base import BaseService
from app.common.utils import password as password_utils
from app.user.exceptions import UserAlreadyReviewedException
from app.user.repositories.user_repository import UserRepository
from app.user.schemas import UserCreate, UserUpdate, UserView
from app.user.schemas.comment import CommentBodyPayload, CommentCreate, CommentView
from app.user.schemas.review import ReviewBodyPayload, ReviewCreate, ReviewView
from app.user.schemas.user import UserCreateHashedPassword
from app.user.services.comment_service import CommentService
from app.user.services.review_service import ReviewService


class UserService(BaseService[UserCreate, UserUpdate, UserView]):
    def __init__(self, db: Session, review_service: ReviewService, comment_service: CommentService):
        super().__init__(
            repository=UserRepository,
            db=db,
        )

        self.review_service = review_service
        self.commment_service = comment_service
        self.aws_repository = AWSRepository(base_path="user")

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

    def profile_comment(
        self,
        comment_body_payload: CommentBodyPayload,
    ) -> CommentView:

        comment_create = CommentCreate(
            comment=comment_body_payload.comment,
            id_user_commented=comment_body_payload.id_user_commented,
            id_user_writer=comment_body_payload.id_user_writer,
        )
        return self.commment_service.create(comment_create)

    def get_user_by_email(self, email: str) -> Users:
        user_repository: UserRepository = self.repository

        user = user_repository.get_user_by_email(email=email)
        return user

    def save_file(self, id_user: UUID, uploaded_file: UploadFile) -> UserView:
        if not (self.get_by_id(id_user=id_user)):
            raise RecordNotFoundException()
        profile_image_url = self.aws_repository.save_file(
            id_obj=id_user, uploaded_file=uploaded_file
        )
        return self.update(id_user=id_user, update=UserUpdate(profile_image=profile_image_url))

    def get_files(self, id_user: UUID) -> List[str]:
        if not (self.get_by_id(id_user=id_user)):
            raise RecordNotFoundException()

        return self.aws_repository.get_files(id_obj=id_user)

    def delete_file(self, id_user: UUID, file_name: str):
        if not (self.get_by_id(id_user=id_user)):
            raise RecordNotFoundException()

        self.aws_repository.delete_file(id_obj=id_user, file_name=file_name)
