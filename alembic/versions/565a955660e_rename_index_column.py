"""rename index column

Revision ID: 565a955660e
Revises: 490994773470
Create Date: 2015-06-20 13:17:03.703498

"""

# revision identifiers, used by Alembic.
revision = '565a955660e'
down_revision = '490994773470'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('current_spreadsheet', 'index')
    op.add_column('current_spreadsheet', sa.Column('indice', sa.Integer))
    pass


def downgrade():
    #op.drop_column('track', 'ind')
    pass
