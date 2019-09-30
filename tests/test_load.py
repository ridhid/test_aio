import asyncpg

from app.settings import Settings
from app.utils.load.update_db import update_db

default_symbols = ['BTC', 'ETH', 'EOS', 'LTC', 'BCH', 'LEO', 'XRP']
settings = Settings()


async def test_load():
    conn = await asyncpg.connect(settings.dsn)
    try:
        await conn.execute('delete from rate')
        await conn.execute('delete from currency')
        await update_db(default_symbols)
        result = await conn.fetchval('select count(*) from currency')
        assert result == len(default_symbols)
    finally:
        await conn.close()
