from urllib.parse import urlparse

from pydantic import BaseSettings


class Settings(BaseSettings):
    name = 'test_aio'
    dsn = 'postgres://test_aio:test_aio@localhost:5432/test_aio'
    load_url = 'https://api-pub.bitfinex.com/v2/candles/trade:1D:t{}USD/hist?limit=10&start={}&end={}&sort=1'

    @property
    def _pg_dsn_parsed(self):
        return urlparse(self.dsn)

    @property
    def pg_name(self):
        return self._pg_dsn_parsed.path.lstrip('/')
