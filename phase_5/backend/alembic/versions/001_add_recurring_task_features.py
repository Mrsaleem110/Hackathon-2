"""Add recurring task and reminder features

Revision ID: 001_add_recurring_task_features
Revises:
Create Date: 2026-02-17 01:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_add_recurring_task_features'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create task_series table for recurring task templates
    op.create_table('task_series',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('recurrence_pattern', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_by_user_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Add columns to tasks table
    op.add_column('tasks', sa.Column('priority', sa.String(), nullable=True))
    op.add_column('tasks', sa.Column('due_date', sa.DateTime(), nullable=True))
    op.add_column('tasks', sa.Column('reminder_time', sa.DateTime(), nullable=True))
    op.add_column('tasks', sa.Column('recurrence_pattern', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('tasks', sa.Column('tags', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('tasks', sa.Column('completed_at', sa.DateTime(), nullable=True))
    op.add_column('tasks', sa.Column('parent_task_id', postgresql.UUID(as_uuid=True), nullable=True))

    # Set default values for existing tasks
    op.execute("UPDATE tasks SET priority = 'medium' WHERE priority IS NULL")
    op.execute("UPDATE tasks SET status = 'active' WHERE status IS NULL")


def downgrade() -> None:
    # Remove columns from tasks table
    op.drop_column('tasks', 'parent_task_id')
    op.drop_column('tasks', 'completed_at')
    op.drop_column('tasks', 'tags')
    op.drop_column('tasks', 'recurrence_pattern')
    op.drop_column('tasks', 'reminder_time')
    op.drop_column('tasks', 'due_date')
    op.drop_column('tasks', 'priority')

    # Drop task_series table
    op.drop_table('task_series')