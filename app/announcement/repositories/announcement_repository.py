from uuid import UUID
from sqlalchemy.orm import Session

import app.common.models as models
from app.common.repositories.base import BaseRepository


class AnnouncementRepository(BaseRepository[models.Announcement, UUID]):
    def __init__(self, db: Session):
        super(AnnouncementRepository, self).__init__(
            models.Announcement.id_announcement,
            model_class=models.Announcement,
            db=db,
        )
    