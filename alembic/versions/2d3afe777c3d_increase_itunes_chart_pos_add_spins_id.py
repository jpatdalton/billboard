"""increase itunes_chart_pos, add spins_id

Revision ID: 2d3afe777c3d
Revises: 3bb654e94bcf
Create Date: 2015-06-19 18:26:19.826890

"""

# revision identifiers, used by Alembic.
revision = '2d3afe777c3d'
down_revision = '3bb654e94bcf'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('track', 'itunes_chart_pos')
    op.add_column('track', sa.Column('itunes_chart_pos', sa.String(7)))
    op.add_column('track', sa.Column('spins_id', sa.String(30)))
    pass


def downgrade():
    op.drop_column('track', 'itunes_chart_pos')
    op.drop_column('track', 'spins_id')
    pass
