"""add_content_column_to_posts_table

Revision ID: 392980b4621f
Revises: 191238603bb5
Create Date: 2022-08-17 15:23:56.822645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '392980b4621f'
down_revision = '191238603bb5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
