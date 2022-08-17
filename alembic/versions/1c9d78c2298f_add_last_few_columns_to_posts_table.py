"""add_last_few_columns_to_posts_table

Revision ID: 1c9d78c2298f
Revises: ee255b33e121
Create Date: 2022-08-17 15:28:37.783500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c9d78c2298f'
down_revision = 'ee255b33e121'
branch_labels = None
depends_on = None



def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
