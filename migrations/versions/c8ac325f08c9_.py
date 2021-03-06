"""empty message

Revision ID: c8ac325f08c9
Revises: 
Create Date: 2018-11-11 20:46:25.214584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8ac325f08c9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('documents',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_uuid', sa.String(length=100), nullable=False),
    sa.Column('filename', sa.String(length=100), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('hash', sa.String(length=255), nullable=True),
    sa.Column('content_type', sa.String(length=20), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documents_filename'), 'documents', ['filename'], unique=False)
    op.create_index(op.f('ix_documents_owner_uuid'), 'documents', ['owner_uuid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_documents_owner_uuid'), table_name='documents')
    op.drop_index(op.f('ix_documents_filename'), table_name='documents')
    op.drop_table('documents')
    # ### end Alembic commands ###
