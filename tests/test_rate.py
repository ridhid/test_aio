import asyncpg

from app.main import create_app
from app.settings import Settings
from tests.test_currencies import test_currencies_success

settings = Settings()


async def test_rate_success(aiohttp_client, loop):
    currencies = await test_currencies_success(aiohttp_client, loop)
    currency = currencies['results']['currencies'][0]['id']
    client = await aiohttp_client(create_app)

    conn = await asyncpg.connect(settings.dsn)
    try:
        resp = await client.get(f'/rate/{currency}/')
        assert resp.status == 200
        result = await resp.json()
        assert 'current_rate' in result
        assert 'avg_volume' in result

        resp = await client.get(f'/rate/?id={currency}')
        assert resp.status == 200
        result = await resp.json()
        assert 'current_rate' in result
        assert 'avg_volume' in result
    finally:
        await conn.close()


async def test_rate_not_found(aiohttp_client, loop):
    curency_name = 'BCH'
    client = await aiohttp_client(create_app)
    conn = await asyncpg.connect(settings.dsn)
    try:
        currency = await conn.fetchval('select id from currency where name=$1', curency_name)
        await conn.execute('delete from currency where name=$1', curency_name)
        resp = await client.get(f'/rate/{currency}/')
        assert resp.status == 404
        result = await resp.json()
        assert 'error' in result
        assert 'detail' in result
        assert 'not found transaction' == result['detail']

    finally:
        await conn.close()


async def test_rate_error(aiohttp_client, loop):
    curency_name = 'BCH'
    client = await aiohttp_client(create_app)
    resp = await client.get(f'/rate/{curency_name}/')
    assert resp.status == 400
