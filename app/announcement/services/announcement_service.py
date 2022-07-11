from sqlalchemy.orm import Session

from app.announcement.repositories.announcement_repository import AnnouncementRepository
from app.announcement.schemas import (
    AnnouncementCreateBodyPayload,
    AnnouncementUpdate,
    AnnouncementView,
)
from app.announcement.schemas.announcement import AnnouncementCreate
from app.announcement.schemas.vacancy import VacancyCreate
from app.announcement.services.address_service import AddressService
from app.announcement.services.vacancy_service import VacancyService
from app.common.services.base import BaseService


class AnnouncementService(
    BaseService[AnnouncementCreateBodyPayload, AnnouncementUpdate, AnnouncementView]
):
    def __init__(
        self, db: Session, vacancy_service: VacancyService, address_service: AddressService
    ):
        super().__init__(
            repository=AnnouncementRepository,
            db=db,
        )
        self.vacancy_service = vacancy_service
        self.address_service = address_service

    def create(self, create: AnnouncementCreateBodyPayload) -> AnnouncementView:
        address = self.address_service.create(create.address)

        announcement_create = AnnouncementCreate(**create.dict(), id_address=address.id_address)

        announcement = self.repository.add(announcement_create)

        vacancies = [
            VacancyCreate(**vacancy.dict(), id_announcement=announcement.id_announcement)
            for vacancy in create.vacancies
        ]

        [self.vacancy_service.create(vacancy) for vacancy in vacancies]

        return announcement
