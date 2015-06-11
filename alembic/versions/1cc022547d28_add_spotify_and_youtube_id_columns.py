"""add spotify and youtube id columns

Revision ID: 1cc022547d28
Revises: 15c384e93ae2
Create Date: 2015-06-07 19:08:26.514839

"""

# revision identifiers, used by Alembic.
revision = '1cc022547d28'
down_revision = '15c384e93ae2'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('track', sa.Column('youtube_id', sa.String(20)))
    op.add_column('track', sa.Column('spotify_id', sa.String(30)))
    pass


def downgrade():
    op.drop_column('track', 'youtube_id')
    op.drop_column('track', 'spotify_id')
    pass
