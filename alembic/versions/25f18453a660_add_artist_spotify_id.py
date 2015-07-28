"""add artist spotify id

Revision ID: 25f18453a660
Revises: 565a955660e
Create Date: 2015-07-24 18:18:30.041108

"""

# revision identifiers, used by Alembic.
revision = '25f18453a660'
down_revision = '565a955660e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('artist', sa.Column('spotify_id', sa.String(25)))

    pass


def downgrade():
    op.drop_column('artist', 'spotify_id')
    pass
