from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1187412e134f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('attendees',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_attendees_email'), 'attendees', ['email'], unique=True)
    op.create_index(op.f('ix_attendees_id'), 'attendees', ['id'], unique=False)
    op.create_index(op.f('ix_attendees_is_deleted'), 'attendees', ['is_deleted'], unique=False)
    op.create_table('venues',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('address', sa.String(length=500), nullable=False),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_venues_city'), 'venues', ['city'], unique=False)
    op.create_index(op.f('ix_venues_id'), 'venues', ['id'], unique=False)
    op.create_index(op.f('ix_venues_is_deleted'), 'venues', ['is_deleted'], unique=False)
    op.create_table('events',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=300), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('start_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('end_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_events_id'), 'events', ['id'], unique=False)
    op.create_index(op.f('ix_events_is_deleted'), 'events', ['is_deleted'], unique=False)
    op.create_index(op.f('ix_events_start_date'), 'events', ['start_date'], unique=False)
    op.create_index(op.f('ix_events_status'), 'events', ['status'], unique=False)
    op.create_index(op.f('ix_events_title'), 'events', ['title'], unique=False)
    op.create_index(op.f('ix_events_venue_id'), 'events', ['venue_id'], unique=False)
    op.create_table('registrations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('attendee_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('registered_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('cancelled_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['attendee_id'], ['attendees.id'], ),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('event_id', 'attendee_id', name='uq_event_attendee')
    )
    op.create_index(op.f('ix_registrations_attendee_id'), 'registrations', ['attendee_id'], unique=False)
    op.create_index(op.f('ix_registrations_event_id'), 'registrations', ['event_id'], unique=False)
    op.create_index(op.f('ix_registrations_id'), 'registrations', ['id'], unique=False)
    op.create_index(op.f('ix_registrations_is_deleted'), 'registrations', ['is_deleted'], unique=False)
    
def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_registrations_is_deleted'), table_name='registrations')
    op.drop_index(op.f('ix_registrations_id'), table_name='registrations')
    op.drop_index(op.f('ix_registrations_event_id'), table_name='registrations')
    op.drop_index(op.f('ix_registrations_attendee_id'), table_name='registrations')
    op.drop_table('registrations')
    op.drop_index(op.f('ix_events_venue_id'), table_name='events')
    op.drop_index(op.f('ix_events_title'), table_name='events')
    op.drop_index(op.f('ix_events_status'), table_name='events')
    op.drop_index(op.f('ix_events_start_date'), table_name='events')
    op.drop_index(op.f('ix_events_is_deleted'), table_name='events')
    op.drop_index(op.f('ix_events_id'), table_name='events')
    op.drop_table('events')
    op.drop_index(op.f('ix_venues_is_deleted'), table_name='venues')
    op.drop_index(op.f('ix_venues_id'), table_name='venues')
    op.drop_index(op.f('ix_venues_city'), table_name='venues')
    op.drop_table('venues')
    op.drop_index(op.f('ix_attendees_is_deleted'), table_name='attendees')
    op.drop_index(op.f('ix_attendees_id'), table_name='attendees')
    op.drop_index(op.f('ix_attendees_email'), table_name='attendees')
    op.drop_table('attendees')