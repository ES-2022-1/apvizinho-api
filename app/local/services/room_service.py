from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.local.repositories.room_repository import RoomRepository
from app.local.schemas import RoomCreate, RoomUpdate, RoomView


class RoomService(BaseService[RoomCreate, RoomUpdate, RoomView]):
    def __init__(self, db: Session):
        super().__init__(
            repository=RoomRepository,
            db=db,
        )
