from uuid import UUID

from sqlalchemy.orm import Session

import app.common.models as models
from app.common.repositories.base import BaseRepository


class AddressRepository(BaseRepository[models.Address, UUID]):
    def __init__(self, db: Session):
        super(AddressRepository, self).__init__(
            models.Address.id_address,
            model_class=models.Address,
            db=db,
        )