from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

# Import app config & models
from app.config import settings
from app.db import Base
from app import models  # import all models so Alembic can see them

# Alembic Config object
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Tell Alembic about our models
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.DATABASE_URL.replace("+asyncpg", "+psycopg2")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    sync_url = settings.DATABASE_URL.replace("+asyncpg", "+psycopg2")

    connectable = create_engine(sync_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
