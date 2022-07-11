from sqlalchemy import Boolean, Column, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Numeric

from app.common.models.table_model import TableModel
from app.db.database import Base


class Vacancy(Base, TableModel):
    __tablename__ = "vacancy"

    id_vacancy = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
        nullable=False,
    )
    id_announcement = Column(
        ForeignKey("announcement.id_announcement", name="vacancy_announcement_fk"),
        nullable=False,
    )

    has_bathroom = Column(Boolean, nullable=False)
    has_garage = Column(Boolean, nullable=False)
    has_furniture = Column(Boolean, nullable=False)
    has_cable_internet = Column(Boolean, nullable=False)
    is_shared_room = Column(Boolean, nullable=False)
    allowed_smoker = Column(Boolean, nullable=False)
    required_organized_person = Column(Boolean, nullable=False)
    required_extroverted_person = Column(Boolean, nullable=False)
    gender = Column(String(50), nullable=True)
    price = Column(Numeric, nullable=False)

    announcement = relationship("Announcement", foreign_keys=id_announcement, lazy="joined")
