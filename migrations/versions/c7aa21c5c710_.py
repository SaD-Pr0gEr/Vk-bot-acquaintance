"""empty message

Revision ID: c7aa21c5c710
Revises: 
Create Date: 2022-04-21 18:32:24.418870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7aa21c5c710'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_country',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('user_gender',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('titles', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('user_status',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('user_town',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('all_vk_users',
    sa.Column('vk_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('surname', sa.String(length=50), nullable=False),
    sa.Column('gender_id', sa.Integer(), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('town_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('is_bot_user', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['user_country.ID'], ),
    sa.ForeignKeyConstraint(['gender_id'], ['user_gender.ID'], ),
    sa.ForeignKeyConstraint(['status_id'], ['user_status.ID'], ),
    sa.ForeignKeyConstraint(['town_id'], ['user_town.ID'], ),
    sa.PrimaryKeyConstraint('vk_id')
    )
    op.create_table('search_params',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('search_owner_id', sa.Integer(), nullable=True),
    sa.Column('age_from', sa.Integer(), nullable=False),
    sa.Column('age_to', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('town', sa.Integer(), nullable=True),
    sa.Column('country', sa.Integer(), nullable=True),
    sa.Column('gender', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['country'], ['user_country.ID'], ),
    sa.ForeignKeyConstraint(['gender'], ['user_gender.ID'], ),
    sa.ForeignKeyConstraint(['search_owner_id'], ['all_vk_users.vk_id'], ),
    sa.ForeignKeyConstraint(['status'], ['user_status.ID'], ),
    sa.ForeignKeyConstraint(['town'], ['user_town.ID'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('search_users',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('search_params_id', sa.Integer(), nullable=True),
    sa.Column('found_result_vk_id', sa.Integer(), nullable=True),
    sa.Column('is_shown', sa.Boolean(), nullable=False),
    sa.Column('liked_status', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['found_result_vk_id'], ['all_vk_users.vk_id'], ),
    sa.ForeignKeyConstraint(['search_params_id'], ['search_params.ID'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('search_users')
    op.drop_table('search_params')
    op.drop_table('all_vk_users')
    op.drop_table('user_town')
    op.drop_table('user_status')
    op.drop_table('user_gender')
    op.drop_table('user_country')
    # ### end Alembic commands ###
