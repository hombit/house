import datetime
import requests
from cachetools.func import ttl_cache
from urllib.parse import urljoin
from .secrets import yandex_api_key


_base_url = 'https://api.rasp.yandex.net/v1.0/search/'


def _days_after_today(x=0):
    today = datetime.date.today()
    day = today + datetime.timedelta(days=x)
    return day.strftime('%Y-%m-%d')


@ttl_cache(50, ttl=900)
def get_rasp(from_station='2001143',
             to_station='2000007',
             lang='ru',
             system='express',
             transport_types='suburban',
             dates=None):
    if dates is None:
        dates = (
            _days_after_today(0),
            _days_after_today(1)
        )
    query_tuple = (
        f'apikey={yandex_api_key}',
        'format=json',
        f'from={from_station}',
        f'to={to_station}',
        f'lang={lang}',
        *(f'date={date}' for date in dates),
        f'system={system}',
        f'transport_types={transport_types}',
    )
    query = '?' + '&'.join(query_tuple)
    url = urljoin(_base_url, query)
    r = requests.get(url)
    return r.json()