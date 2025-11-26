"""Create phno. for users column

Revision ID: ee6fd0b15fb4
Revises: 
Create Date: 2025-11-25 15:33:33.427358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee6fd0b15fb4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('Phone_No', sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'Phone No')
