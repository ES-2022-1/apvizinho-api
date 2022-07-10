from sqlalchemy import Column, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Numeric
from app.common.models.table_model import TableModel
from app.db.database import Base


class Room(Base, TableModel):
    __tablename__ = "room"

    id_room = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
        nullable=False,
    )
    id_local = Column(
        ForeignKey("local.id_local", name="room_local_fk"),
        nullable=False,
    )
    has_bathroom = Column(bool, nullable=False)
    has_garage = Column(bool, nullable=False)
    has_furniture = Column(bool, nullable=False)
    has_cable_internet = Column(bool, nullable=False)
    is_shared_room = Column(bool, nullable=False)
    allowed_smoker = Column(bool, nullable=False)
    required_organized_person = Column(bool, nullable=False)
    required_ectroverted_person = Column(bool, nullable=False)
    gender = Column(String(50), nullable=True)
    price = Column(Numeric, nullable=False)
