"""create_user_table

Revision ID: eceef3913549
Revises:
Create Date: 2022-07-10 14:13:05.107381

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "eceef3913549"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column(
            "id_user",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("firstname", sa.String(length=50), nullable=False),
        sa.Column("surname", sa.String(length=50), nullable=False),
        sa.Column("password_hash", sa.String(length=50), nullable=False),
        sa.Column("cellphone", sa.String(length=13), nullable=False),
        sa.Column("document", sa.String(length=11), nullable=False),
        sa.Column("birthdate", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id_user"),
        sa.UniqueConstraint("id_user"),
    )


def downgrade():
    op.drop_table("user")
