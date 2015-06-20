"""change integer to string

Revision ID: dbd8f2c992c
Revises: 605a1252173
Create Date: 2015-06-14 21:41:54.304928

"""

# revision identifiers, used by Alembic.
revision = 'dbd8f2c992c'
down_revision = '605a1252173'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('track', 'shazam_id')
    op.drop_column('track', 'itunes_id')
    op.add_column('track', sa.Column('shazam_id', sa.String(20)))
    op.add_column('track', sa.Column('itunes_id', sa.String(20)))
    pass


def downgrade():
    op.drop_column('track', 'shazam_id')
    op.drop_column('track', 'itunes_id')
    pass
