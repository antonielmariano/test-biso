import time
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.exc import OperationalError
from alembic import context
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext

from app.core.config import settings
from app.db.base import engine

def check_database_ready(retries=5, delay=2):
    for attempt in range(retries):
        try:
            with engine.connect() as connection:
                return True
        except OperationalError as e:
            if attempt == retries - 1: 
                raise Exception(
                    f"Database not ready after {retries} attempts: {str(e)}"
                )
            wait = delay * (2 ** attempt)
            print(f"Database not ready. Waiting {wait} seconds...")
            time.sleep(wait)
    return False

def run_migrations():
    check_database_ready()
    alembic_cfg = Config("alembic.ini")
    script = ScriptDirectory.from_config(alembic_cfg)
    
    with engine.connect() as connection:
        context = MigrationContext.configure(connection)
        if context.get_current_revision() != script.get_current_head():
            print("Running database migrations...")
            fileConfig(alembic_cfg.config_file_name)
            alembic_cfg.attributes['connection'] = connection
            command.upgrade(alembic_cfg, "head")
            print("Migrations completed successfully!")
        else:
            print("Database is up to date!") 