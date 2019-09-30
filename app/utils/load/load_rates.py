import argparse
import asyncio

from app.utils.load.update_db import update_db

default_symbols = ['BTC', 'ETH', 'EOS', 'LTC', 'BCH', 'LEO', 'XRP']
parser = argparse.ArgumentParser(description='Заполняем бд данными')
parser.add_argument('--symbols', metavar='N', type=str, nargs='+',
                    help=f'Валюты по дефолту {" ".join(default_symbols)}',
                    default=default_symbols)
args = parser.parse_args()


def load():
    loop = asyncio.get_event_loop()

    loop.run_until_complete(update_db(args.symbols))


if __name__ == '__main__':
    load()
