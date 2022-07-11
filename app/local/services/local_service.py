from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.local.repositories.local_repository import LocalRepository
from app.local.schemas import LocalCreate, LocalUpdate, LocalView
from app.local.schemas.local import LocalCreateBodyPayload
from app.local.schemas.room import RoomCreate
from app.local.services.address_service import AddressService
from app.local.services.room_service import RoomService


class LocalService(BaseService[LocalCreateBodyPayload, LocalUpdate, LocalView]):
    def __init__(self, db: Session, room_service: RoomService, address_service: AddressService):
        super().__init__(
            repository=LocalRepository,
            db=db,
        )
        self.room_service = room_service
        self.address_service = address_service

    def create(self, create: LocalCreateBodyPayload) -> LocalView:
        address = self.address_service.create(create.address)

        local_create = LocalCreate(**create.dict(), id_address=address.id_address)

        local = self.repository.add(local_create)

        rooms = [RoomCreate(**room.dict(), id_local=local.id_local) for room in create.rooms]

        [self.room_service.create(room) for room in rooms]

        return local
