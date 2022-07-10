from sqlalchemy import Column, String, Text, text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.schema import ForeignKey
from app.common.models.table_model import TableModel
from app.db.database import Base


class Local(Base, TableModel):
    __tablename__ = "Local"

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
    rooms = relationship(
        "Room",
        primaryjoin="and_(Local.id_local==Room.id_local, "
        "Room.deleted_at.is_(None))",
        backref="local",
    )
    id_address = Column(
        ForeignKey("Address.id_address", name="local_address_fk"),
        nullable=False,
    )
    address = relationship("Address", foreign_keys=id_address, lazy="joined")

    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    is_close_to_university = Column(Boolean, nullable=False)
    is_close_to_supermarket = Column(Boolean, nullable=False)
    has_furniture = Column(Boolean, nullable=False)
    has_internet = Column(Boolean, nullable=False)
    allow_pet = Column(Boolean, nullable=False)
    allow_events = Column(Boolean, nullable=False)
    has_piped_gas = Column(Boolean, nullable=False)
    type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)

