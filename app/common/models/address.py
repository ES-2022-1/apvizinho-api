from sqlalchemy import Column, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import Numeric

from app.common.models.table_model import TableModel
from app.db.database import Base


class Address(Base, TableModel):
    __tablename__ = "address"

    id_address = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
        nullable=False,
    )
    street = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)
    number = Column(String(50), nullable=True)
    complement = Column(String(50), nullable=True)
    zip_code = Column(String(50), nullable=True)
    latitude = Column(Numeric, nullable=True)
    longitude = Column(Numeric, nullable=True)
