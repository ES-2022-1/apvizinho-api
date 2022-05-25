"""create todo it

Revision ID: d5997645d810
Revises:
Create Date: 2022-05-23 20:35:37.218841

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "d5997645d810"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "todo_list",
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column(
            "id_todo_list",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("nome", sa.String(length=50), nullable=False),
        sa.Column("prazo", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id_todo_list"),
        sa.UniqueConstraint("id_todo_list"),
    )


def downgrade():
    op.drop_table("todo_list")
