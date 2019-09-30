import sqlalchemy as sa
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from sqlalchemy import func

from app.models import RateOrm
from app.schema.currency import Currency
from app.schema.rate import Rate
from app.utils.basic_auth import auth


async def return_value(currency: Currency, pool):
    query = sa.select([RateOrm.rate.label('current_rate'), func.avg(RateOrm.volume).label('avg_volume')]).group_by(
        RateOrm.id).where(RateOrm.currency_id == currency.id).order_by(RateOrm.date.desc()).limit(1)
    async with pool.transaction() as conn:
        result = await conn.fetchrow(query)
        if result is None:
            return Response(text='not found transaction', status=404)
        result = Rate(**dict(result))
        return Response(body=result.json().encode('utf-8'), content_type='application/json', status=200)


@auth.required
async def rate_query(request: Request):
    currency = Currency(**request.query)
    return await return_value(currency, request.app['pool'])


@auth.required
async def rate_url(request: Request):
    currency = Currency(**request.match_info)
    return await return_value(currency, request.app['pool'])
