from alembic import op

# revision identifiers, used by Alembic.
revision = '0ec153695de7'
down_revision = '4cfe2d52fccc'
branch_labels = None
depends_on = None

def upgrade():
    op.drop_constraint(
        'numeros_suspeitos_suspeito_id_fkey',
        'numeros_suspeitos',
        type_='foreignkey'
    )

    op.create_foreign_key(
        'numeros_suspeitos_suspeito_id_fkey',
        'numeros_suspeitos',
        'suspeitos',
        ['suspeito_id'],
        ['id'],
        ondelete='CASCADE'
    )

def downgrade():
    op.drop_constraint(
        'numeros_suspeitos_suspeito_id_fkey',
        'numeros_suspeitos',
        type_='foreignkey'
    )

    op.create_foreign_key(
        'numeros_suspeitos_suspeito_id_fkey',
        'numeros_suspeitos',
        'suspeitos',
        ['suspeito_id'],
        ['id']
    )
