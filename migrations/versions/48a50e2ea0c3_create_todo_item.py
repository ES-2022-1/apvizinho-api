"""create todo item

Revision ID: 48a50e2ea0c3
Revises: d5997645d810
Create Date: 2022-05-23 20:39:56.316753

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "48a50e2ea0c3"
down_revision = "d5997645d810"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "todo_item",
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column(
            "id_todo_item",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("nome", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=250), nullable=False),
        sa.Column("id_todo_list", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_todo_list"], ["todo_list.id_todo_list"], name="todo_item_todo_list_fk"
        ),
        sa.PrimaryKeyConstraint("id_todo_item"),
        sa.UniqueConstraint("id_todo_item"),
    )
    op.create_unique_constraint(None, "todo_list", ["id_todo_list"])


def downgrade():
    op.drop_constraint(None, "todo_list", type_="unique")
    op.drop_table("todo_item")
