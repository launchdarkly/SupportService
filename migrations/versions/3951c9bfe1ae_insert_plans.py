"""insert plans

Revision ID: 3951c9bfe1ae
Revises: 07c695b8cd68
Create Date: 2018-12-20 12:39:21.246895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3951c9bfe1ae'
down_revision = '07c695b8cd68'
branch_labels = None
depends_on = None


def upgrade():
    # create all plans
    op.execute("INSERT INTO plan (id, name, description, cost) VALUES (1, 'free', 'All the basic features of SupportService.', 0)") 
    op.execute("INSERT INTO plan (id, name, description, cost) VALUES (2, 'bronze', 'Everything in free and email support.', 25)") 
    op.execute("INSERT INTO plan (id, name, description, cost) VALUES (3, 'silver', 'Everything in bronze and chat support.', 50)") 
    op.execute("INSERT INTO plan (id, name, description, cost) VALUES (4, 'gold', 'Everything in silver and 99.999% uptime SLA!', 100)") 
    # give everyone a free plan by default
    op.execute('UPDATE plan SET created_date=NOW()')
    op.execute('UPDATE plan SET updated_date=NOW()')
    op.execute('UPDATE public.user SET plan_id=1')
    pass


def downgrade():
    pass
