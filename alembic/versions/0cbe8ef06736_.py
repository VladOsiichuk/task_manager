"""empty message

Revision ID: 0cbe8ef06736
Revises: cf81ef3b7c52
Create Date: 2019-11-20 21:17:56.663458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0cbe8ef06736"
down_revision = "cf81ef3b7c52"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "users", ["email"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="unique")
    # ### end Alembic commands ###