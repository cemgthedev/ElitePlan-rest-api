"""tornando campos obrigatórios em user

Revision ID: 0d6f040b69e0
Revises: 91e2b398a4c4
Create Date: 2024-12-29 11:59:27.031731

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d6f040b69e0'
down_revision: Union[str, None] = '91e2b398a4c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
