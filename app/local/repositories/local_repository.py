from uuid import UUID

from sqlalchemy.orm import Session

import app.common.models as models
from app.common.repositories.base import BaseRepository


class LocalRepository(BaseRepository[models.Local, UUID]):
    def __init__(self, db: Session):
        super(LocalRepository, self).__init__(
            models.Local.id_local,
            model_class=models.Local,
            db=db,
        )
