"""add current spreadsheet

Revision ID: 5e53461f7d0
Revises: 1e72846fd5c6
Create Date: 2015-06-17 19:55:34.855972

"""

# revision identifiers, used by Alembic.
revision = '5e53461f7d0'
down_revision = '1e72846fd5c6'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey


def upgrade():
    op.create_table(
        'current_spreadsheet',
        sa.Column('track_id', sa.Integer, ForeignKey('track.id'))
    )
    pass


def downgrade():
    op.drop_table('current_spreadsheet')
    pass
