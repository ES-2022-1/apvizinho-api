from uuid import UUID

from sqlalchemy.orm import Session

import app.common.models as models
from app.common.repositories.base import BaseRepository


class RoomRepository(BaseRepository[models.Room, UUID]):
    def __init__(self, db: Session):
        super(RoomRepository, self).__init__(
            models.Room.id_room,
            model_class=models.Room,
            db=db,
        )
