"""user_profile_image_bio

Revision ID: 75194bfba77b
Revises: 88848f7bc0d2
Create Date: 2022-07-23 18:54:48.753726

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "75194bfba77b"
down_revision = "88848f7bc0d2"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("profile_image", sa.Text(), nullable=True))
    op.add_column("users", sa.Column("bio", sa.Text(), nullable=True))


def downgrade():
    op.drop_column("users", "bio")
    op.drop_column("users", "profile_image")
