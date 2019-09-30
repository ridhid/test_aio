import asyncpgsa
import uvloop
from aiohttp import web

from app.utils.db import prepare_database
from app.utils.exception_middleware import error_middleware
from app.views.currencies import currencies
from app.views.rate import rate_url, rate_query
from .settings import Settings

uvloop.install()


async def startup(app: web.Application):
    settings: Settings = app['settings']
    await prepare_database(settings, False)
    app['pool'] = await asyncpgsa.create_pool(settings.dsn, min_size=2)


async def cleanup(app: web.Application):
    await app['pool'].close()


def create_app(loop=None):
    if loop is not None:  # pragma: no cover
        app = web.Application(middlewares=[error_middleware], loop=loop)
    else:
        app = web.Application(middlewares=[error_middleware])
    settings = Settings()
    app.update(
        settings=settings,
    )

    app.on_startup.append(startup)
    app.on_cleanup.append(cleanup)

    app.add_routes([
        web.get('/currencies', currencies),
        web.get('/rate/', rate_query),
        web.get('/rate/{id}/', rate_url),
    ])

    return app
