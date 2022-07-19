from sqlalchemy import Boolean, Column, String, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.announcement.schemas.announcement import AnnouncementStatus
from app.common.models.table_model import TableModel
from app.db.database import Base


class Announcement(Base, TableModel):
    __tablename__ = "announcement"

    id_announcement = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
        nullable=False,
    )
    id_user = Column(
        ForeignKey("users.id_user", name="announcement_user_fk"),
        nullable=False,
    )
    id_address = Column(
        ForeignKey("address.id_address", name="announcement_address_fk"),
        nullable=False,
    )

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
    status = Column(String(50), nullable=False, default=AnnouncementStatus.ACTIVE)

    address = relationship("Address", foreign_keys=id_address, lazy="joined")

    user = relationship("Users", foreign_keys=id_user, lazy="joined")

    vacancies = relationship(
        "Vacancy",
        primaryjoin="and_(Announcement.id_announcement==Vacancy.id_announcement, "
        "Announcement.deleted_at.is_(None))",
    )
