"""radio audience int -> string

Revision ID: 3bb654e94bcf
Revises: 5e53461f7d0
Create Date: 2015-06-19 18:09:24.628002

"""

# revision identifiers, used by Alembic.
revision = '3bb654e94bcf'
down_revision = '5e53461f7d0'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('track', 'radio_audience')
    op.add_column('track', sa.Column('radio_audience', sa.String(7)))
    pass


def downgrade():
    op.drop_column('track', 'radio_audience')
    pass
