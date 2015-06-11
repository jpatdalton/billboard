"""soundcloud id

Revision ID: 605a1252173
Revises: 1cc022547d28
Create Date: 2015-06-09 22:57:29.570459

"""

# revision identifiers, used by Alembic.
revision = '605a1252173'
down_revision = '1cc022547d28'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('artist', 'soundloud_id')
    op.add_column('artist', sa.Column('soundcloud_id', sa.String(20)))
    pass


def downgrade():
    op.add_column('artist', sa.Column('soundloud_id', sa.String(20)))
    op.drop_column('artist', 'soundloud_id')
    pass
