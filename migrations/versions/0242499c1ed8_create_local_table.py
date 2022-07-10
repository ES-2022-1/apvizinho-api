"""create_local_table

Revision ID: 0242499c1ed8
Revises: eceef3913549
Create Date: 2022-07-10 17:39:40.711579

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0242499c1ed8'
down_revision = 'eceef3913549'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Address',
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('id_address', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('street', sa.String(length=50), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('number', sa.String(length=50), nullable=True),
    sa.Column('complement', sa.String(length=50), nullable=True),
    sa.Column('zip_code', sa.String(length=50), nullable=True),
    sa.Column('latitude', sa.Numeric(), nullable=True),
    sa.Column('longitude', sa.Numeric(), nullable=True),
    sa.PrimaryKeyConstraint('id_address'),
    sa.UniqueConstraint('id_address')
    )
    op.create_table('Local',
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('id_local', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('id_user', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('id_address', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('is_close_to_university', sa.Boolean(), nullable=False),
    sa.Column('is_close_to_supermarket', sa.Boolean(), nullable=False),
    sa.Column('has_furniture', sa.Boolean(), nullable=False),
    sa.Column('has_internet', sa.Boolean(), nullable=False),
    sa.Column('allow_pet', sa.Boolean(), nullable=False),
    sa.Column('allow_events', sa.Boolean(), nullable=False),
    sa.Column('has_piped_gas', sa.Boolean(), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['id_address'], ['Address.id_address'], name='local_address_fk'),
    sa.ForeignKeyConstraint(['id_user'], ['user.id_user'], name='local_user_fk'),
    sa.PrimaryKeyConstraint('id_local'),
    sa.UniqueConstraint('id_local')
    )
    op.create_table('Room',
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('id_room', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('id_local', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('has_bathroom', sa.Boolean(), nullable=False),
    sa.Column('has_garage', sa.Boolean(), nullable=False),
    sa.Column('has_furniture', sa.Boolean(), nullable=False),
    sa.Column('has_cable_internet', sa.Boolean(), nullable=False),
    sa.Column('is_shared_room', sa.Boolean(), nullable=False),
    sa.Column('allowed_smoker', sa.Boolean(), nullable=False),
    sa.Column('required_organized_person', sa.Boolean(), nullable=False),
    sa.Column('required_ectroverted_person', sa.Boolean(), nullable=False),
    sa.Column('gender', sa.String(length=50), nullable=True),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.ForeignKeyConstraint(['id_local'], ['Local.id_local'], name='room_local_fk'),
    sa.PrimaryKeyConstraint('id_room'),
    sa.UniqueConstraint('id_room')
    )

def downgrade():
    op.drop_table('Room')
    op.drop_table('Local')
    op.drop_table('Address')
