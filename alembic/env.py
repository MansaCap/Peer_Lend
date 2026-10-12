import os
import sys
from logging.config import fileConfig
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from alembic import context

# -----------------------------------------------------------------------------
# 1. Load environment variables from .env
# -----------------------------------------------------------------------------
root_dir = Path(__file__).resolve().parent.parent
backend_dir = root_dir / "peer_lending_backend"
src_dir = backend_dir / "src"

for env_path in [root_dir / ".env", backend_dir / ".env", src_dir / ".env"]:
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        break
else:
    load_dotenv()

# Add backend and src directories to sys.path so modules can be imported
for p in [str(src_dir), str(backend_dir), str(root_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# -----------------------------------------------------------------------------
# 2. Import Base and DATABASE_URL from db.database
# -----------------------------------------------------------------------------
from db.database import Base, DATABASE_URL

# -----------------------------------------------------------------------------
# 3. Import models to register table schemas on Base.metadata
# -----------------------------------------------------------------------------
import models  # Loads all models (users, loans, collateral, repayments, transactions,
               # borrower_payback_status, payback_analysis_tally, notifications)

# -----------------------------------------------------------------------------
# Alembic Config
# -----------------------------------------------------------------------------
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -----------------------------------------------------------------------------
# 4. Configure metadata for autogenerate
# -----------------------------------------------------------------------------
target_metadata = Base.metadata

# Override sqlalchemy.url with DATABASE_URL from db.database if provided
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine,
    emitting the generated SQL script to output.
    """
    url = config.get_main_option("sqlalchemy.url") or DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section, {})
    if DATABASE_URL:
        configuration["sqlalchemy.url"] = DATABASE_URL

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
