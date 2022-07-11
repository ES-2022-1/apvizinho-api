"""update_table_names

Revision ID: a4414bedc4c4
Revises: 0242499c1ed8
Create Date: 2022-07-11 19:04:28.574527

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "a4414bedc4c4"
down_revision = "0242499c1ed8"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "address",
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column(
            "id_address",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("street", sa.String(length=50), nullable=True),
        sa.Column("city", sa.String(length=50), nullable=True),
        sa.Column("number", sa.String(length=50), nullable=True),
        sa.Column("complement", sa.String(length=50), nullable=True),
        sa.Column("zip_code", sa.String(length=50), nullable=True),
        sa.Column("latitude", sa.Numeric(), nullable=True),
        sa.Column("longitude", sa.Numeric(), nullable=True),
        sa.PrimaryKeyConstraint("id_address"),
        sa.UniqueConstraint("id_address"),
    )
    op.create_table(
        "announcement",
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column(
            "id_announcement",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("id_user", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("id_address", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("is_close_to_university", sa.Boolean(), nullable=False),
        sa.Column("is_close_to_supermarket", sa.Boolean(), nullable=False),
        sa.Column("has_furniture", sa.Boolean(), nullable=False),
        sa.Column("has_internet", sa.Boolean(), nullable=False),
        sa.Column("allow_pet", sa.Boolean(), nullable=False),
        sa.Column("allow_events", sa.Boolean(), nullable=False),
        sa.Column("has_piped_gas", sa.Boolean(), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_address"], ["address.id_address"], name="announcement_address_fk"
        ),
        sa.ForeignKeyConstraint(["id_user"], ["user.id_user"], name="announcement_user_fk"),
        sa.PrimaryKeyConstraint("id_announcement"),
        sa.UniqueConstraint("id_announcement"),
    )
    op.create_table(
        "vacancy",
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column(
            "id_vacancy",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("id_announcement", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("has_bathroom", sa.Boolean(), nullable=False),
        sa.Column("has_garage", sa.Boolean(), nullable=False),
        sa.Column("has_furniture", sa.Boolean(), nullable=False),
        sa.Column("has_cable_internet", sa.Boolean(), nullable=False),
        sa.Column("is_shared_room", sa.Boolean(), nullable=False),
        sa.Column("allowed_smoker", sa.Boolean(), nullable=False),
        sa.Column("required_organized_person", sa.Boolean(), nullable=False),
        sa.Column("required_extroverted_person", sa.Boolean(), nullable=False),
        sa.Column("gender", sa.String(length=50), nullable=True),
        sa.Column("price", sa.Numeric(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_announcement"], ["announcement.id_announcement"], name="vacancy_announcement_fk"
        ),
        sa.PrimaryKeyConstraint("id_vacancy"),
        sa.UniqueConstraint("id_vacancy"),
    )
    op.drop_constraint("room_local_fk", "Room")
    op.drop_table("Local")
    op.drop_table("Address")
    op.drop_table("Room")


def downgrade():
    op.create_table(
        "Room",
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
            "id_room",
            postgresql.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("id_local", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column("has_bathroom", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("has_garage", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("has_furniture", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("has_cable_internet", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("is_shared_room", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("allowed_smoker", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("required_organized_person", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("required_extroverted_person", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("gender", sa.VARCHAR(length=50), autoincrement=False, nullable=True),
        sa.Column("price", sa.NUMERIC(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(["id_local"], ["Local.id_local"], name="room_local_fk"),
        sa.PrimaryKeyConstraint("id_room", name="Room_pkey"),
    )
    op.create_table(
        "Address",
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
            "id_address",
            postgresql.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("street", sa.VARCHAR(length=50), autoincrement=False, nullable=True),
        sa.Column("city", sa.VARCHAR(length=50), autoincrement=False, nullable=True),
        sa.Column("number", sa.VARCHAR(length=50), autoincrement=False, nullable=True),
        sa.Column("complement", sa.VARCHAR(length=50), autoincrement=False, nullable=True),
        sa.Column("zip_code", sa.VARCHAR(length=50), autoincrement=False, nullable=True),
        sa.Column("latitude", sa.NUMERIC(), autoincrement=False, nullable=True),
        sa.Column("longitude", sa.NUMERIC(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id_address", name="Address_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "Local",
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
            "id_local",
            postgresql.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("id_user", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column("id_address", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column("title", sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.Column("description", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column("is_close_to_university", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("is_close_to_supermarket", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("has_furniture", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("has_internet", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("allow_pet", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("allow_events", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("has_piped_gas", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("type", sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.Column("status", sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(["id_address"], ["Address.id_address"], name="local_address_fk"),
        sa.ForeignKeyConstraint(["id_user"], ["user.id_user"], name="local_user_fk"),
        sa.PrimaryKeyConstraint("id_local", name="Local_pkey"),
    )
    op.drop_table("vacancy")
    op.drop_table("announcement")
    op.drop_table("address")
