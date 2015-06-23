"""add indices to current_spreadsheet

Revision ID: 490994773470
Revises: 2d3afe777c3d
Create Date: 2015-06-20 13:02:04.030454

"""

# revision identifiers, used by Alembic.
revision = '490994773470'
down_revision = '2d3afe777c3d'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('current_spreadsheet', sa.Column('index', sa.Integer))
    pass


def downgrade():
    op.drop_column('current_spreadsheet', 'index')
    pass
