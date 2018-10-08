import datetime
import sys
import time
from decimal import Decimal

import requests

from cmc_db import Session
from cmc_model import GlobalTokenHistory

probe_frequency = 30


def coinmarketcap_dump():
    n = 100
    c = 200
    i = 1
    l = []
    try:
        while i <= c:
            r = requests.get('https://api.coinmarketcap.com/v2/ticker/', timeout=10,
                             params={'convert': 'BTC', 'start': i, 'limit': n}).json()
            c = r['metadata']['num_cryptocurrencies']
            for (k, v) in r['data'].items():
                l.append((v['symbol'], v['quotes']['BTC']['price'], v['quotes']['USD']['price']))
            i += n
            print(len(l))
            time.sleep(1)
        return l
    except:
        return l


def coinpaprika_dump():
    l = []
    try:
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.40 Safari/537.36'})
        data = requests.get('https://api.coinpaprika.com/v1/ticker', headers=headers, timeout=60).json()
        for v in data:
            l.append((v['id'], v['symbol'], Decimal(v['price_btc']) if v['price_btc'] else None,
                      Decimal(v['price_usd']) if v['price_usd'] else None,
                      Decimal(v['volume_24h_usd']) if v['volume_24h_usd'] else None))
        return l
    except:
        return l


def nn(*args):
    for e in args:
        if e is not None:
            return e
    return None


def one():
    try:
        ts = datetime.datetime.now()
        print('{} start'.format(ts))
        session = Session()
        data = coinpaprika_dump()
        count = 0
        for (token_id, token, price_btc, price_usd, volume) in data:
            last = session.query(GlobalTokenHistory).filter(
                GlobalTokenHistory.token_id == token_id).order_by(GlobalTokenHistory.ts.desc()).first()
            if nn(token, '') != '' and nn(token_id, '') != '':
                if (last is None) or (
                        nn(last.price_btc, 0) != nn(price_btc, 0)
                        or nn(last.price_usd, 0) != nn(price_usd, 0)
                        or nn(last.volume_24h_usd, 0) != nn(volume, 0)):
                    count += 1
                    session.add(
                        GlobalTokenHistory(ts=ts, token_id=token_id, token=token, price_btc=price_btc,
                                           price_usd=price_usd,
                                           volume_24h_usd=volume))
        session.commit()
        session.close()
        print('{} all:{} new:{}'.format(datetime.datetime.now(), len(data), count))
        return True
    except Exception as err:
        sys.stderr.write('ERROR: %sn' % str(err))


def loop():
    while True:
        one()
        time.sleep(probe_frequency)


if __name__ == '__main__':
    loop()
