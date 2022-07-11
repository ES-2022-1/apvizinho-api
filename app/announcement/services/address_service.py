from sqlalchemy.orm import Session

from app.announcement.repositories.address_repository import AddressRepository
from app.announcement.schemas import AddressCreate, AddressUpdate, AddressView
from app.common.lib.google_address_api import GoogleAddressApi
from app.common.services.base import BaseService


class AddressService(BaseService[AddressCreate, AddressUpdate, AddressView]):
    def __init__(self, db: Session):
        super().__init__(
            repository=AddressRepository,
            db=db,
        )

    def create(self, create: AddressCreate) -> AddressView:
        google_api = GoogleAddressApi()
        coordinates = google_api.get_location_coordinates(
            street=create.street, city=create.city, zip_code=create.zip_code
        )
        create.latitude = coordinates[0]
        create.longitude = coordinates[1]

        return self.repository.add(create)
