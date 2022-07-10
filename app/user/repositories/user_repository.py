from uuid import UUID

from sqlalchemy.orm import Session

import app.common.models as models
from app.common.repositories.base import BaseRepository


<<<<<<< HEAD:app/local/repositories/address_repository.py
class AddressRepository(BaseRepository[models.Address, UUID]):
    def __init__(self, db: Session):
        super(AddressRepository, self).__init__(
            models.Address.id_address,
            model_class=models.Address,
=======
class UserRepository(BaseRepository[models.User, UUID]):
    def __init__(self, db: Session):
        super(UserRepository, self).__init__(
            models.User.id_user,
            model_class=models.User,
>>>>>>> 8f061e98089539a6f61d3d5bfb2e46835e306427:app/user/repositories/user_repository.py
            db=db,
        )
