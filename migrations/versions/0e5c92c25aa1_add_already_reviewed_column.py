"""add_already_reviewed_column

Revision ID: 0e5c92c25aa1
Revises: 19928e06eb94
Create Date: 2022-07-12 00:11:02.666970

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0e5c92c25aa1"
down_revision = "19928e06eb94"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("already_reviewed", sa.Boolean(), nullable=True))
    op.execute("UPDATE users SET already_reviewed = false")
    op.alter_column(table_name="users", column_name="already_reviewed", nullable=False)


def downgrade():
    op.drop_column("users", "already_reviewed")
