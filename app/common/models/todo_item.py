from sqlalchemy import Column, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.common.models.table_model import TableModel
from app.db.database import Base


class TodoItem(Base, TableModel):
    __tablename__ = "todo_item"

    id_todo_item = Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
        nullable=False,
    )

    nome = Column(String(50), nullable=False)
    description = Column(String(250), nullable=False)

    id_todo_list = Column(
        ForeignKey("todo_list.id_todo_list", name="todo_item_todo_list_fk"),
        nullable=False,
    )
    todo_list = relationship("TodoList", foreign_keys=id_todo_list)
