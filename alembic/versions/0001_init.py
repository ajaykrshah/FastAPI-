from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    run_status = sa.Enum('Pending','Running','Failed','Completed', name='run_status')
    run_status.create(op.get_bind(), checkfirst=True)

    op.create_table('product',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default=sa.sql.expression.true()),
        sa.Column('cron', sa.Text(), nullable=True),
        sa.Column('status', run_status, nullable=False, server_default='Pending'),
        sa.Column('last_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
    )
    op.create_index('idx_product_enabled', 'product', ['enabled'])
    op.create_index('idx_product_status', 'product', ['status'])
    op.create_index('idx_product_metadata', 'product', ['metadata'], postgresql_using='gin')

    op.create_table('execution_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('product.id', ondelete="CASCADE"), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('status', run_status, nullable=False, server_default='Pending'),
        sa.Column('pipeline_run_id', sa.Text(), nullable=True),
        sa.Column('duration_ms', sa.BigInteger(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
    )
    op.create_index('idx_hist_status', 'execution_history', ['status'])
    op.create_index('idx_hist_product', 'execution_history', ['product_id'])
    op.create_index('idx_hist_created', 'execution_history', ['created_at'])

    op.create_table('execution_step',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('history_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('execution_history.id', ondelete="CASCADE"), nullable=False),
        sa.Column('sequence', sa.Integer(), nullable=False),
        sa.Column('step_name', sa.String(), nullable=False),
        sa.Column('scripting', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column('script_output', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column('status', run_status, nullable=False, server_default='Pending'),
        sa.Column('started_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('finished_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.UniqueConstraint('history_id', 'sequence')
    )

def downgrade() -> None:
    op.drop_table('execution_step')
    op.drop_index('idx_hist_created', table_name='execution_history')
    op.drop_index('idx_hist_product', table_name='execution_history')
    op.drop_index('idx_hist_status', table_name='execution_history')
    op.drop_table('execution_history')
    op.drop_index('idx_product_metadata', table_name='product')
    op.drop_index('idx_product_status', table_name='product')
    op.drop_index('idx_product_enabled', table_name='product')
    op.drop_table('product')
    sa.Enum(name='run_status').drop(op.get_bind(), checkfirst=False)
