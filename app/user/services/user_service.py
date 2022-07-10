from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.user.repositories.user_repository import UserRepository
from app.user.schemas import UserCreate, UserUpdate, UserView


class UserService(BaseService[UserCreate, UserUpdate, UserView]):
    def __init__(self, db: Session):
        super().__init__(
            repository=UserRepository,
            db=db,
        )
