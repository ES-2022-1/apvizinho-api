from uuid import UUID

from sqlalchemy.orm import Session

import app.common.models as models
from app.common.exceptions import RecordNotFoundException
from app.common.repositories.base import BaseRepository


class UserRepository(BaseRepository[models.Users, UUID]):
    def __init__(self, db: Session):
        super(UserRepository, self).__init__(
            models.Users.id_user,
            model_class=models.Users,
            db=db,
        )

    def get_user_by_email(self, email: str) -> models.Users:
        model = self.default_query.filter(self.model_class.email == email).first()
        if not model:
            raise RecordNotFoundException()
        return model
