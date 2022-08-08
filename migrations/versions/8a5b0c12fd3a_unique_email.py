"""unique_email

Revision ID: 8a5b0c12fd3a
Revises: 75194bfba77b
Create Date: 2022-08-08 02:19:29.832310

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "8a5b0c12fd3a"
down_revision = "75194bfba77b"
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(
        constraint_name="users_uk", table_name="users", columns=["id_user", "email"]
    )


def downgrade():
    op.drop_constraint(constraint_name="users_uk", table_name="users")
