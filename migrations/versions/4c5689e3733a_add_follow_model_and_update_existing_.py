from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection

# revision identifiers, used by Alembic.
revision = '4c5689e3733a'
down_revision = '73a27fd1892a'
branch_labels = None
depends_on = None

def upgrade():
    # Bind to the current engine
    bind = op.get_bind()
    inspector = reflection.Inspector.from_engine(bind)

    # Check if the 'follows' table already exists
    if 'follows' not in inspector.get_table_names():
        op.create_table('follows',
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('artist_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_follows_user'),
            sa.ForeignKeyConstraint(['artist_id'], ['user.id'], name='fk_follows_artist'),
            sa.PrimaryKeyConstraint('user_id', 'artist_id', name='pk_follows')
        )

    # Add 'artwork_id' column to 'comment' table with a named foreign key constraint
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('artwork_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_comment_artwork',  # Name the foreign key constraint
            'artwork',  # Target table
            ['artwork_id'],  # Source column
            ['id']  # Target column
        )

def downgrade():
    # Remove 'artwork_id' column from 'comment' table
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint('fk_comment_artwork', type_='foreignkey')
        batch_op.drop_column('artwork_id')

    # Drop the 'follows' table
    op.drop_table('follows')
