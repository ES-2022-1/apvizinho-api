from uuid import UUID

from sqlalchemy.orm import Session

import app.common.models as models
from app.common.repositories.base import BaseRepository


class UserRepository(BaseRepository[models.User, UUID]):
    def __init__(self, db: Session):
        super(UserRepository, self).__init__(
            models.User.id_user,
            model_class=models.User,
            db=db,
        )