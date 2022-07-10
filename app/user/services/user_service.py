from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.common.utils import password as password_utils
from app.user.repositories.user_repository import UserRepository
from app.user.schemas import UserCreate, UserUpdate, UserView
from app.user.schemas.user import UserCreateHashedPassword


class UserService(BaseService[UserCreate, UserUpdate, UserView]):
    def __init__(self, db: Session):
        super().__init__(
            repository=UserRepository,
            db=db,
        )

    def create(self, create: UserCreate) -> UserView:
        user_create = UserCreateHashedPassword(
            **create.dict(), password_hash=password_utils.create_hash(create.password)
        )

        return self.repository.add(user_create)
