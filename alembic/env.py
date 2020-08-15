from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from sqlalchemy.engine.url import URL
from alembic import context

from tools.database import BASE
from tools.database.models import *
from tools.config import DATABASE_CONFIG

config = context.config

fileConfig(config.config_file_name)

target_metadata = BASE.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    connectable = create_engine(URL(**DATABASE_CONFIG))
    with connectable.connect() as conn:
        context.configure(
            connection=conn, target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(URL(**DATABASE_CONFIG))
    with connectable.connect() as conn:
        context.configure(
            connection=conn, target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
