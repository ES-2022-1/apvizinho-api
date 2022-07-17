from sqlalchemy import Column, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.schema import ForeignKey

from app.common.models.table_model import TableModel
from app.db.database import Base


class Profile_Comment(Base, TableModel):

    __tablename__ = "profile_comment"

    id_comment = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
        nullable=False,
    )

    id_user_commented = Column(
        ForeignKey("users.id_user", name="commented_user_fk"), nullable=False, unique=True
    )
    id_user_writer = Column(
        ForeignKey("users.id_user", name="writer_user_fk"), nullable=False, unique=True
    )
    comment = Column(Text, nullable=False)
    UniqueConstraint("id_comment", "id_user_commented", "id_user_writer", name="comment_ak_01")
