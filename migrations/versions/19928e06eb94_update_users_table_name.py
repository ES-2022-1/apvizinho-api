"""update_users_table_name

Revision ID: 19928e06eb94
Revises: a4414bedc4c4
Create Date: 2022-07-12 00:05:02.298351

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "19928e06eb94"
down_revision = "a4414bedc4c4"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
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
        sa.Column("password_hash", sa.String(length=100), nullable=False),
        sa.Column("cellphone", sa.String(length=13), nullable=False),
        sa.Column("document", sa.String(length=11), nullable=False),
        sa.Column("birthdate", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id_user"),
        sa.UniqueConstraint("id_user"),
    )
    op.drop_constraint("announcement_user_fk", "announcement", type_="foreignkey")
    op.drop_table("user")
    op.create_foreign_key("announcement_user_fk", "announcement", "users", ["id_user"], ["id_user"])


def downgrade():
    op.drop_constraint("announcement_user_fk", "announcement", type_="foreignkey")
    op.create_foreign_key("announcement_user_fk", "announcement", "user", ["id_user"], ["id_user"])
    op.create_table(
        "user",
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("deleted_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column(
            "id_user",
            postgresql.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("email", sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.Column("firstname", sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.Column("surname", sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.Column("password_hash", sa.VARCHAR(length=100), autoincrement=False, nullable=False),
        sa.Column("cellphone", sa.VARCHAR(length=13), autoincrement=False, nullable=False),
        sa.Column("document", sa.VARCHAR(length=11), autoincrement=False, nullable=False),
        sa.Column("birthdate", sa.DATE(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id_user", name="user_pkey"),
    )
    op.drop_table("users")
