"""add a lot of columns to track

Revision ID: 1e72846fd5c6
Revises: dbd8f2c992c
Create Date: 2015-06-17 19:46:37.089392

"""

# revision identifiers, used by Alembic.
revision = '1e72846fd5c6'
down_revision = 'dbd8f2c992c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('track', sa.Column('writers', sa.String(250)))
    op.add_column('track', sa.Column('producers', sa.String(100)))
    op.add_column('track', sa.Column('label', sa.String(80)))
    op.add_column('track', sa.Column('spins_diff', sa.Integer))
    op.add_column('track', sa.Column('spins_pop_pos', sa.String(3)))
    op.add_column('track', sa.Column('spins_pop', sa.String(8)))
    op.add_column('track', sa.Column('spins_rhythmic', sa.String(8)))
    op.add_column('track', sa.Column('spins_urban', sa.String(8)))
    op.add_column('track', sa.Column('itunes_chart_pos', sa.String(3)))
    pass


def downgrade():
    op.drop_column('track', 'writers')
    op.drop_column('track', 'producers')
    op.drop_column('track', 'label')
    op.drop_column('track', 'spins_diff')
    op.drop_column('track', 'spins_pop_pos')
    op.drop_column('track', 'spins_pop')
    op.drop_column('track', 'spins_rhythmic')
    op.drop_column('track', 'spins_urban')
    op.drop_column('track', 'itunes_chart_pos')
    pass
