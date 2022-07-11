from uuid import UUID

from sqlalchemy.orm import Session

import app.common.models as models
from app.common.repositories.base import BaseRepository


class VacancyRepository(BaseRepository[models.Vacancy, UUID]):
    def __init__(self, db: Session):
        super(VacancyRepository, self).__init__(
            models.Vacancy.id_vacancy,
            model_class=models.Vacancy,
            db=db,
        )
