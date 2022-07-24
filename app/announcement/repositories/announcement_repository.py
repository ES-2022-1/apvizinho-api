from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

import app.common.models as models
from app.common.models.announcement import Announcement
from app.common.repositories.base import BaseFinder, BaseRepository


class AnnouncementFinder(BaseFinder[models.Announcement]):
    @classmethod
    def get_instance(cls, db: Session):
        return cls((db.query(models.Announcement).filter(models.Announcement.deleted_at.is_(None))))

    def filtered_by_id_user(self, id_user: UUID):
        if id_user:
            return AnnouncementFinder(
                self.base_query.filter(models.Announcement.id_user == id_user)
            )


class AnnouncementRepository(BaseRepository[models.Announcement, UUID]):
    def __init__(self, db: Session):
        super(AnnouncementRepository, self).__init__(
            models.Announcement.id_announcement,
            model_class=models.Announcement,
            db=db,
            finder=AnnouncementFinder,
        )

    def get_announcements_by_id_user(self, id_user: UUID) -> List[Announcement]:
        finder: AnnouncementFinder = self.finder
        return finder.filtered_by_id_user(id_user=id_user).all()
