import math

import sqlalchemy as sa
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from sqlalchemy import func

from app.models import CurrencyOrm
from app.schema.currency import CurrencyList
from app.schema.pagination import PaginationRequest, get_pagination_response
from app.utils.basic_auth import auth

currency_pagination = get_pagination_response(CurrencyList)


@auth.required
async def currencies(request: Request):
    pagination = PaginationRequest(**request.query)
    query = sa.select([CurrencyOrm]).limit(pagination.size).offset(pagination.offset)
    count = sa.select([func.count(CurrencyOrm.id)])
    async with request.app['pool'].transaction() as conn:
        result = await conn.fetch(query)
        total = await conn.fetchval(count)
        result = [dict(elem) for elem in result]
        currency_list = CurrencyList(currencies=result)
        next_page = pagination.page + 1 if (pagination.page + 1) <= math.ceil(total / pagination.size) else None
        prev_page = pagination.page - 1 if pagination.page - 1 > 0 else None
        resp = currency_pagination(total=total,
                                   results=currency_list,
                                   next_page=next_page, prev_page=prev_page)
        return Response(body=resp.json().encode('utf-8'), content_type='application/json', status=200)
