import asyncpg

from app.main import create_app
from app.settings import Settings

settings = Settings()


async def test_currencies_success(aiohttp_client, loop):
    client = await aiohttp_client(create_app)
    conn = await asyncpg.connect(settings.dsn)
    try:
        resp = await client.get('/currencies')
        assert resp.status == 200
        result = await resp.json()
        assert 'total' in result
        assert 'results' in result
        assert 'next_page' in result
        assert 'prev_page' in result
        assert result['prev_page'] is None
        assert result['next_page'] == 2
        total = result['total']
        count = await conn.fetchval('select count(*) from currency')
        assert count == total

        return result
    finally:
        await conn.close()


async def test_currencies_next(aiohttp_client, loop):
    result1 = await test_currencies_success(aiohttp_client, loop)
    client = await aiohttp_client(create_app)
    conn = await asyncpg.connect(settings.dsn)
    try:
        resp = await client.get(f'/currencies?page={result1["next_page"]}')
        assert resp.status == 200
        result = await resp.json()
        assert result['results'] != result1['results']
    finally:
        await conn.close()


async def test_currencies_size_gt_2(aiohttp_client, loop):
    client = await aiohttp_client(create_app)
    conn = await asyncpg.connect(settings.dsn)
    try:
        resp = await client.get('/currencies?size=5')
        assert resp.status == 200
        result = await resp.json()
        assert 'total' in result
        assert 'results' in result
        assert 'next_page' in result
        assert 'prev_page' in result
        assert result['prev_page'] is None
        assert result['next_page'] == 2
        total = result['total']
        count = await conn.fetchval('select count(*) from currency')
        assert count == total

        return result
    finally:
        await conn.close()
