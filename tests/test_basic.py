import sys

from app.main import create_app


async def test_basic(aiohttp_client, loop):
    client = await aiohttp_client(create_app)
    del sys._called_from_test
    resp = await client.get('/currencies')
    assert resp.status == 401
    sys._called_from_test = True
