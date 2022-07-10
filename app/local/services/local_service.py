from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.local.repositories.local_repository import LocalRepository
from app.local.schemas import LocalCreate, LocalUpdate, LocalView


class LocalService(BaseService[LocalCreate, LocalUpdate, LocalView]):
    def __init__(self, db: Session):
        super().__init__(
            repository=LocalRepository,
            db=db,
        )
