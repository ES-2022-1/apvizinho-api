from typing import List
from uuid import UUID

from fastapi import UploadFile
from haversine import haversine
from sqlalchemy.orm import Session

from app.announcement.repositories.announcement_repository import AnnouncementRepository
from app.announcement.schemas import (
    AnnouncementCreateBodyPayload,
    AnnouncementUpdate,
    AnnouncementView,
)
from app.announcement.schemas.announcement import (
    AnnouncementCreate,
    AnnouncementFilter,
    AnnouncementTagsEnum,
)
from app.announcement.schemas.vacancy import GenderEnum, VacancyCreate
from app.announcement.services.address_service import AddressService
from app.announcement.services.vacancy_service import VacancyService
from app.common.exceptions import RecordNotFoundException
from app.common.repositories.aws_repository import AWSRepository
from app.common.services.base import BaseService
from app.common.utils.constants import RADIUS, UFCG_COORDINATES


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
        self.aws_repository = AWSRepository(base_path="announcement")

    def get_by_id(self, **kwargs) -> AnnouncementView:
        announcement = super().get_by_id(**kwargs)

        announcement.images_url = self.get_files(id_announcement=announcement.id_announcement)

        return announcement

    def get_all(self) -> List[AnnouncementView]:
        annoucements = super().get_all()

        for announcement in annoucements:
            announcement.images_url = self.get_files(id_announcement=announcement.id_announcement)

        return annoucements

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

    def filter(self, announcement_filter: AnnouncementFilter) -> List[AnnouncementView]:
        all_announcements = self.get_all()
        ranked_announcements = dict()
        filters = announcement_filter.filters
        filters = list(reversed(filters))

        for announcement in all_announcements:
            score = self.__calculate_announcement_score(announcement, filters)
            ranked_announcements[announcement] = score

        ranked_announcements = dict(
            sorted(ranked_announcements.items(), key=lambda item: item[1], reverse=True)
        )
        announcements = list(ranked_announcements.keys())

        return announcements

    def save_file(self, id_announcement: UUID, uploaded_file: UploadFile) -> str:
        if not (self.get_by_id(id_announcement=id_announcement)):
            raise RecordNotFoundException()
        return self.aws_repository.save_file(id_obj=id_announcement, uploaded_file=uploaded_file)

    def save_multiple_files(
        self, id_announcement: UUID, uploaded_files: List[UploadFile]
    ) -> List[str]:
        if not (self.get_by_id(id_announcement=id_announcement)):
            raise RecordNotFoundException()
        self.aws_repository.save_multiple_files(
            id_obj=id_announcement, uploaded_files=uploaded_files
        )

    def get_files(self, id_announcement: UUID) -> List:
        return self.aws_repository.get_files(id_obj=id_announcement)

    def delete_file(self, id_announcement: UUID, file_name: str):
        if not (self.get_by_id(id_announcement=id_announcement)):
            raise RecordNotFoundException()

        self.aws_repository.delete_file(id_obj=id_announcement, file_name=file_name)

    def get_announcements_by_id_user(self, id_user: UUID) -> List[AnnouncementView]:
        repository: AnnouncementRepository = self.repository

        annoucements = repository.get_announcements_by_id_user(id_user=id_user)

        for announcement in annoucements:
            announcement.images_url = self.get_files(id_announcement=announcement.id_announcement)

        return annoucements

    def __calculate_announcement_score(self, announcement: AnnouncementView, filters: list):
        true_items = self.__extract_true_items(announcement)
        matched, match_score = self.__get_matched_items(filters, true_items)

        m = len(matched)
        n = len(filters)

        announcement_coordinates = (announcement.address.latitude, announcement.address.longitude)
        d = haversine(UFCG_COORDINATES, announcement_coordinates)

        score = ((m / n) * match_score) + (RADIUS - (d / RADIUS))

        return score

    def __extract_true_items(self, announcement: AnnouncementView):

        true_items = list()

        if announcement.allow_events:
            true_items.append(AnnouncementTagsEnum.ALLOW_EVENTS)
        if announcement.allow_pet:
            true_items.append(AnnouncementTagsEnum.ALLOW_PETS)
        if announcement.has_furniture:
            true_items.append(AnnouncementTagsEnum.HAS_FURNITURE)
        if announcement.has_internet:
            true_items.append(AnnouncementTagsEnum.HAS_INTERNET)
        if announcement.has_piped_gas:
            true_items.append(AnnouncementTagsEnum.HAS_PIPED_GAS)
        if announcement.is_close_to_supermarket:
            true_items.append(AnnouncementTagsEnum.IS_CLOSE_TO_SUPERMARKET)
        if announcement.is_close_to_university:
            true_items.append(AnnouncementTagsEnum.IS_CLOSE_TO_UNIVERSITY)

        for vacancy in announcement.vacancies:
            if vacancy.allowed_smoker:
                true_items.append(AnnouncementTagsEnum.ALLOWED_SMOKER)
            if vacancy.has_bathroom:
                true_items.append(AnnouncementTagsEnum.HAS_BATHROOM)
            if vacancy.has_cable_internet:
                true_items.append(AnnouncementTagsEnum.HAS_CABLE_INTERNET)
            if vacancy.is_shared_room:
                true_items.append(AnnouncementTagsEnum.IS_SHARED_ROOM)
            if vacancy.required_extroverted_person:
                true_items.append(AnnouncementTagsEnum.REQUIRED_EXTROVERTED_PERSON)
            if vacancy.required_organized_person:
                true_items.append(AnnouncementTagsEnum.REQUIRED_ORGANIZED_PERSON)

            if vacancy.gender == GenderEnum.FEMALE:
                true_items.append(AnnouncementTagsEnum.FEMALE_GENDER)
            elif vacancy.gender == GenderEnum.MALE:
                true_items.append(AnnouncementTagsEnum.MALE_GENDER)

        return true_items

    def __get_matched_items(self, filters, items):
        matched = list()
        match_score = 0

        for i in range(len(filters)):
            filter = filters[i]
            if filter in items:
                matched.append(filter)
                match_score += i

        if (
            (AnnouncementTagsEnum.MALE_GENDER in filters)
            and (AnnouncementTagsEnum.MALE_GENDER not in matched)
        ) or (
            (AnnouncementTagsEnum.FEMALE_GENDER in filters)
            and (AnnouncementTagsEnum.FEMALE_GENDER not in matched)
        ):
            match_score = match_score / 2

        return matched, match_score
