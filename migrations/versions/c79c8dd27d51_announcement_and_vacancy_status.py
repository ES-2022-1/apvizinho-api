"""announcement_and_vacancy_status

Revision ID: c79c8dd27d51
Revises: 101e055f082a
Create Date: 2022-07-18 22:35:29.372795

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c79c8dd27d51"
down_revision = "101e055f082a"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "vacancy", sa.Column("status", sa.String(length=50), nullable=True, server_default="EMPTY")
    )
    op.execute("UPDATE vacancy SET status = 'FULLFILLED'")
    op.alter_column(table_name="vacancy", column_name="status", nullable=False)
    op.execute("UPDATE announcement SET status = 'DISABLED'")
    op.alter_column("announcement", "status", server_default="ACTIVE")


def downgrade():
    op.drop_column("vacancy", "status")
