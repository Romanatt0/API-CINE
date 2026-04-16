"""refactor_favorite_films_add_film_id_fk

Revision ID: 8a9c1e7492c1
Revises: a082b677b41e
Create Date: 2026-04-15 19:30:47.509367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a9c1e7492c1'
down_revision: Union[str, Sequence[str], None] = 'a082b677b41e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Refatora favorite_films:
    - Remove coluna film_name (string livre)
    - Adiciona film_id (FK para films.id, NOT NULL)
    - Garante user_id NOT NULL
    """
    with op.batch_alter_table('favorite_films', recreate='always') as batch_op:
        batch_op.drop_column('film_name')
        batch_op.add_column(sa.Column('film_id', sa.Integer(), nullable=False, server_default='0'))
        batch_op.alter_column('user_id', existing_type=sa.INTEGER(), nullable=False)
        batch_op.create_foreign_key('fk_favorite_films_film_id', 'films', ['film_id'], ['id'])

    # Remove o server_default após criação (não é mais necessário)
    with op.batch_alter_table('favorite_films') as batch_op:
        batch_op.alter_column('film_id', existing_type=sa.INTEGER(), server_default=None)


def downgrade() -> None:
    """Reverte para o schema original com film_name."""
    with op.batch_alter_table('favorite_films', recreate='always') as batch_op:
        batch_op.drop_constraint('fk_favorite_films_film_id', type_='foreignkey')
        batch_op.drop_column('film_id')
        batch_op.add_column(sa.Column('film_name', sa.VARCHAR(), nullable=False, server_default=''))
        batch_op.alter_column('user_id', existing_type=sa.INTEGER(), nullable=True)
