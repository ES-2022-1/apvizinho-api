from sqlalchemy import Column, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from app.common.models.table_model import TableModel
from app.db.database import Base


class TodoList(Base, TableModel):
    __tablename__ = "todo_list"

    id_todo_list = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
        nullable=False,
    )

    nome = Column(String(50), nullable=False)
    prazo = Column(DateTime, nullable=False)

    items = relationship(
        "TodoItem",
        primaryjoin="and_(TodoList.id_todo_list==TodoItem.id_todo_list, "
        "TodoItem.deleted_at.is_(None))",
        backref="todo_list",
    )
