"""add_review_table

Revision ID: 101e055f082a
Revises: 0e5c92c25aa1
Create Date: 2022-07-12 00:38:26.087159

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "101e055f082a"
down_revision = "0e5c92c25aa1"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "review",
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column(
            "id_review",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("id_user", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("comment", sa.Text(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["id_user"], ["users.id_user"], name="review_user_fk"),
        sa.PrimaryKeyConstraint("id_review"),
        sa.UniqueConstraint("id_review"),
        sa.UniqueConstraint("id_user"),
    )


def downgrade():
    op.drop_table("review")
