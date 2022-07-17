from sqlalchemy.orm import Session
from haversine import haversine

from app.announcement.repositories.announcement_repository import AnnouncementRepository
from app.announcement.schemas import (
    AnnouncementCreateBodyPayload,
    AnnouncementUpdate,
    AnnouncementView,
)
from app.announcement.schemas import announcement
from app.announcement.schemas.announcement import AnnouncementCreate, AnnouncementFilter
from app.announcement.schemas.vacancy import GenderEnum, VacancyCreate
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

    def filter(self, announcement_filter:AnnouncementFilter):
        all_announcements = self.get_all()
        ranked_announcements = dict()
        filters = announcement_filter.filters
        filters = list(reversed(filters))

        for announcement in all_announcements:
            score = self.__calculate_announcement_score(announcement, filters)
            ranked_announcements[announcement] = score

        ranked_announcements = dict(sorted(ranked_announcements.items(), key=lambda item: item[1]))
        announcements = list(ranked_announcements.keys())

        return announcements


    def __calculate_announcement_score(self, announcement:AnnouncementView, filters:list):
        true_items = self.__extract_true_items(announcement)
        matched, match_score = self.__get_matched_items(filters, true_items)
        
        m = len(matched)
        n = len(filters)

        UFCG_COORDINATES = (-7.216945, -35.909722) #TODO - Colocar esse dado em um arquivo de constantes
        R = 1
        announcement_coordinates = (announcement.address.latitude,announcement.address.longitude)
        d = haversine(UFCG_COORDINATES, announcement_coordinates)

        return ((m/n) * match_score) + (R - (d/R))


    def __extract_true_items(self, announcement:AnnouncementView):

        #TODO - Criar um ENUM para esses itens

        true_items = list()

        if announcement.allow_events:
            true_items.append("ALLOW_EVENTS")
        if announcement.allow_pet:
            true_items.append("ALLOW_PETS")
        if announcement.has_furniture:
            true_items.append("HAS_FORNITURE")
        if announcement.has_internet:
            true_items.append("HAS_INTERNET")
        if announcement.has_piped_gas:
            true_items.append("HAS_PIPED_GAS")
        if announcement.is_close_to_supermarket:
            true_items.append("IS_CLOSE_TO_SUPERMARKET")
        if announcement.is_close_to_university:
            true_items.append("IS_CLOSE_TO_UNIVERSITY")
        
        for vacancy in announcement.vacancies:
            if vacancy.allowed_smoker:
                true_items.append("ALLOWED_SMOKER")
            if vacancy.has_bathroom:
                true_items.append("HAS_BATHROOM")
            if vacancy.has_cable_internet:
                true_items.append("HAS_CABLE_INTERNET")
            if vacancy.is_shared_room:
                true_items.append("IS_SHARED_ROOM")
            if vacancy.required_extroverted_person:
                true_items.append("REQUIRED_EXTROVERTED_PERSON")
            
            if vacancy.gender == GenderEnum.FEMALE:
                true_items.append("FEMALE_GENDER")
            elif vacancy.gender == GenderEnum.MALE:
                true_items.append("MALE_GENDER")
        
        return true_items

    def __get_matched_items(self, filters, items):
        matched = list()
        match_score = 0
        
        for i in range(len(filters)):
            filter = filters[i]
            if filter in items:
                matched.append(filters)
                match_score += i

        return matched, match_score