from sqlalchemy import Column, Integer, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.common.models.table_model import TableModel
from app.db.database import Base


class Review(Base, TableModel):
    __tablename__ = "review"

    id_review = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
        nullable=False,
    )

    id_user = Column(
        ForeignKey("users.id_user", name="review_user_fk"), nullable=False, unique=True
    )

    comment = Column(Text, nullable=False)
    score = Column(Integer, nullable=False)

    user = relationship("Users", foreign_keys=id_user, lazy="joined")

    UniqueConstraint("id_review", "id_user", name="review_ak_01")
