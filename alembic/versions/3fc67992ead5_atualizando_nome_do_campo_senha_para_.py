"""Atualizando nome do campo senha para password

Revision ID: 3fc67992ead5
Revises: 86f2aac783cd
Create Date: 2024-12-29 21:10:06.943275

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic
revision: str = '3fc67992ead5'
down_revision: Union[str, None] = '86f2aac783cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Renomeia a coluna de 'senha' para 'password', preservando dados e tipo
    op.alter_column(
        'users',                  # Nome da tabela
        'senha',                  # Nome da coluna antiga
        new_column_name='password',  # Novo nome da coluna
        existing_type=sa.String(),  # Tipo existente da coluna
        nullable=False            # Propriedade de nulabilidade
    )


def downgrade() -> None:
    # Reverte a renomeação de 'password' para 'senha'
    op.alter_column(
        'users',
        'password',
        new_column_name='senha',
        existing_type=sa.String(),
        nullable=False
    )
