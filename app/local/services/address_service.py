from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.local.repositories.address_repository import AddressRepository
from app.local.schemas import AddressCreate, AddressUpdate, AddressView


class AddressService(BaseService[AddressCreate, AddressUpdate, AddressView]):
    def __init__(self, db: Session):
        super().__init__(
            repository=AddressRepository,
            db=db,
        )
