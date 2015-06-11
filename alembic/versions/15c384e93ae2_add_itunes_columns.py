"""add itunes columns

Revision ID: 15c384e93ae2
Revises: 3fc409fe0baa
Create Date: 2015-06-07 17:52:26.831412

"""

# revision identifiers, used by Alembic.
revision = '15c384e93ae2'
down_revision = '3fc409fe0baa'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('track', sa.Column('itunes_id', sa.Integer))
    op.add_column('track', sa.Column('itunes_release_date', sa.DateTime))
    pass


def downgrade():
    op.drop_column('track', 'itunes_id')
    op.drop_column('track', 'itunes_release_date')
    pass
