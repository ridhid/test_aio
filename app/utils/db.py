from pathlib import Path

import asyncpg

from app.settings import Settings

THIS_DIR = Path(__file__).parent
DROP_CONNECTIONS = """
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = $1 AND pid <> pg_backend_pid()
"""


async def prepare_database(settings: Settings, overwrite_existing: bool) -> bool:
    """
    (Re)create a fresh database and run migrations.

    Partially taken from https://github.com/samuelcolvin/aiohttp-toolbox/blob/master/atoolbox/db/__init__.py

    :param settings: settings to use for db connection
    :param overwrite_existing: whether or not to drop an existing database if it exists
    :return: whether or not a database has been (re)created
    """
    no_db_dsn, _ = settings.dsn.rsplit('/', 1)
    conn = await asyncpg.connect(dsn=no_db_dsn)
    try:
        if not overwrite_existing:
            # don't drop connections and try creating a db if it already exists and we're not overwriting
            exists = await conn.fetchval('SELECT 1 AS result FROM pg_database WHERE datname=$1', settings.pg_name)
            if exists:
                return False

        await conn.execute(DROP_CONNECTIONS, settings.pg_name)
    finally:
        await conn.close()
