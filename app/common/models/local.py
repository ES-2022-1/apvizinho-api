from sqlalchemy import Column, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.schema import ForeignKey
from app.common.models.table_model import TableModel
from app.db.database import Base


class Local(Base, TableModel):
    __tablename__ = "local"

    id_local = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
        nullable=False,
    )
    id_user = Column(
        ForeignKey("user.id_user", name="local_user_fk"),
        nullable=False,
    )
    id_room = rooms = relationship(
        "Romm",
        primaryjoin="and_(Local.local==Romm.id_romm, "
        "Room.deleted_at.is_(None))",
        backref="local",
    )
    id_address = Column(
        ForeignKey("address.id_address", name="local_address_fk"),
        nullable=False,
    )
    title = Column(String(50), nullable=False)
    description = Column(text, nullable=False)
    is_close_to_university = Column(bool, nullable=False)
    is_close_to_supermarket = Column(bool, nullable=False)
    has_furniture = Column(bool, nullable=False)
    has_internet = Column(bool, nullable=False)
    allow_pet = Column(bool, nullable=False)
    allow_events = Column(bool, nullable=False)
    has_piped_gas = Column(bool, nullable=False)
    type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)

