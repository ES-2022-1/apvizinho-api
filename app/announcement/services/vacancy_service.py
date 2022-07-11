from sqlalchemy.orm import Session

from app.announcement.repositories.vacancy_repository import VacancyRepository
from app.announcement.schemas.vacancy import VacancyCreate, VacancyUpdate, VacancyView
from app.common.services.base import BaseService


class VacancyService(BaseService[VacancyCreate, VacancyUpdate, VacancyView]):
    def __init__(self, db: Session):
        super().__init__(
            repository=VacancyRepository,
            db=db,
        )
