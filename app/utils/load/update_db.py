import datetime

import aiohttp
import asyncpg
import asyncpgsa
import sqlalchemy as sa
from dateutil.relativedelta import relativedelta
from dateutil.tz import tzutc
from tqdm import tqdm

from app.models import CurrencyOrm, RateOrm
from app.settings import Settings


def unix_time_millis(dt: datetime.datetime) -> int:
    """
    Конвертируем в милиссек
    :param d: datetime.date дата
    :return: int
    """
    return int(dt.timestamp() * 1000)


current_date_gt = datetime.datetime.now(tzutc())
current_date_10 = unix_time_millis(current_date_gt + relativedelta(days=-10))
current_date_gt = unix_time_millis(current_date_gt)
settings = Settings()


async def update_db(symbols):
    conn = await asyncpg.connect(settings.dsn)
    try:
        async with aiohttp.ClientSession() as session:
            for symbol in tqdm(symbols):
                async with conn.transaction():
                    insert = sa.insert(CurrencyOrm).values(name=symbol).returning(CurrencyOrm.id)
                    query_string, params = asyncpgsa.compile_query(insert)
                    async with session.get(settings.load_url.format(symbol, current_date_10, current_date_gt)) as resp:
                        result = await resp.json()
                        if resp.status != 200:  # pragma: no cover
                            print(f'error {symbol}, {result}')  # pragma: no cover
                            continue  # pragma: no cover
                        currency_id = await conn.fetchval(query_string, *params)
                        if len(result) == 0:
                            print(f'transaction {symbol} not found')
                            continue
                        insert = sa.insert(RateOrm)
                        values = []
                        for val in result:
                            _date, rate, volume = datetime.date.fromtimestamp(val[0] // 1000), val[2], val[5]
                            values.append({
                                'currency_id': currency_id,
                                'date': _date,
                                'rate': rate,
                                'volume': volume,
                            })
                        insert = insert.values(values)
                        query_string, params = asyncpgsa.compile_query(insert)
                        await conn.execute(query_string, *params)
    finally:
        await conn.close()
