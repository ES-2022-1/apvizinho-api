from typing import List
from uuid import UUID, uuid4
from xmlrpc.client import boolean

from haversine import haversine
from sqlalchemy.orm import Session
import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile
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
from app.common.services.base import BaseService
from app.common.utils.constants import RADIUS, UFCG_COORDINATES
from app.common.exceptions import RecordNotFoundException
from app.core.settings import AWS_BUCKET_NAME


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
        self.s3 = boto3.client("s3")

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

    def save_file(self, id_announcement: UUID, uploaded_file: UploadFile) -> boolean:
        if not self.get_by_id(id_announcement=id_announcement):
            raise RecordNotFoundException()
        if not uploaded_file.filename.startswith("~"):
            try:
                file_name = uuid4().hex + ".jpg"
                file_path = f"{str(id_announcement)}/images/{file_name}"
                self.s3.upload_fileobj(
                    uploaded_file.file,
                    AWS_BUCKET_NAME,
                    file_path,
                )
                return f"https://{AWS_BUCKET_NAME}.s3.us-east-1.amazonaws.com/{file_path}"
            except ClientError as e:
                print("S3 Credentials is not valid")
                return False
                print(e)
            except Exception as e:
                print("Error: ", e)
                return False

    def save_multiple_files(
        self, id_announcement: UUID, uploaded_files: List[UploadFile]
    ) -> boolean:
        return [self.save_file(id_announcement, uploaded_file) for uploaded_file in uploaded_files]

    def get_files(self, id_announcement: UUID) -> List:
        if not self.get_by_id(id_announcement=id_announcement):
            raise RecordNotFoundException()
        bucket = self.__get_bucket_data()
        response = []
        if bucket:
            for obj in bucket["Contents"]:
                if obj["Key"].startswith(f"{str(id_announcement)}/images"):
                    response.append(
                        f"https://{AWS_BUCKET_NAME}.s3.us-east-1.amazonaws.com/{obj['Key']}"
                    )
        return response

    def delete_file(self, id_announcement: UUID, file_name: str) -> boolean:
        if not self.get_by_id(id_announcement=id_announcement):
            raise RecordNotFoundException()
        file_path = f"{str(id_announcement)}/images/{file_name}"
        try:
            self.s3.delete_object(Bucket=AWS_BUCKET_NAME, Key=file_path)
            return True
        except ClientError as e:
            print("S3 Credentials is not valid")
            print(e)
        except Exception as e:
            print("Error: ", e)
            return False

    def __get_bucket_data(self) -> dict:
        try:
            response = self.s3.list_objects_v2(
                Bucket=AWS_BUCKET_NAME,
                EncodingType="url",
                FetchOwner=True,
                RequestPayer="requester",
            )
            return response
        except ClientError as e:
            print("S3 Credentials is not valid")
            print(e)
        except Exception as e:
            print("Error: ", e)
            print(e)

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
