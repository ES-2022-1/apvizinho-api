from sqlalchemy import Boolean, Column, Date, String, Text, text
from sqlalchemy.dialects.postgresql import UUID

from app.common.models.table_model import TableModel
from app.db.database import Base


class Users(Base, TableModel):
    __tablename__ = "users"

    id_user = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
        nullable=False,
    )

    email = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    password_hash = Column(String(100), nullable=False)
    cellphone = Column(String(13), nullable=False)
    document = Column(String(11), nullable=False)
    birthdate = Column(Date, nullable=False)
    already_reviewed = Column(Boolean, nullable=False, default=False)
    profile_image = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
