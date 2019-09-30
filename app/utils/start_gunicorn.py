import asyncio
import multiprocessing

from aiohttp import GunicornWebWorker
from gunicorn.app.base import BaseApplication

from app.main import create_app


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


bind = '%s:%s' % ('0.0.0.0', '8000')


class StandaloneApplication(BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in self.options.items()
                       if key in self.cfg.settings and value is not None])
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def runserver():
    options = {
        'bind': bind,
        'workers': number_of_workers(),
        'worker_class': 'aiohttp.GunicornUVLoopWebWorker',
    }
    app = create_app()
    StandaloneApplication(app, options).run()


if __name__ == "__main__":
    runserver()
