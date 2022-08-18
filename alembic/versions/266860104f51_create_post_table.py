"""create post table

Revision ID: 266860104f51
Revises: 
Create Date: 2022-08-17 15:20:04.452362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '266860104f51'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
