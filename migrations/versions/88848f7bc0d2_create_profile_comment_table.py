"""create_profile_comment_table

Revision ID: 88848f7bc0d2
Revises: 101e055f082a
Create Date: 2022-07-17 15:11:15.737005

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "88848f7bc0d2"
down_revision = "101e055f082a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "profile_comment",
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column(
            "id_comment",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("id_user_commented", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("id_user_writer", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("comment", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["id_user_commented"], ["users.id_user"], name="commented_user_fk"),
        sa.ForeignKeyConstraint(["id_user_writer"], ["users.id_user"], name="writer_user_fk"),
        sa.PrimaryKeyConstraint("id_comment"),
        sa.UniqueConstraint("id_comment"),
        sa.UniqueConstraint("id_user_commented"),
        sa.UniqueConstraint("id_user_writer"),
    )


def downgrade():
    op.drop_table("profile_comment")
