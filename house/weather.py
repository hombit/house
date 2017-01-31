import requests
from urllib.parse import urljoin
from functools import reduce
from cachetools.func import ttl_cache
from .secrets import weather_underground_api_key


_base_url = 'https://api.wunderground.com/api/'


@ttl_cache(500, ttl=720)
def get_weather(location='Russia/Moscow',
                lang='RU',
                features=('conditions','forecast','astronomy')):
    url_parts = (
        f'{weather_underground_api_key}/',
        *(f'{f}/' for f in features),
        f'lang%3A{lang}/',
        'q/',
        f'{location}.json'
    )
    url = reduce(urljoin, url_parts, _base_url)
    r = requests.get(url)
    return r.json()


def wind(mph):
    return '{:.1f}'.format(float(mph) / 3.6).replace('.', ',')


def wind_dir(s, NESW='СВЮЗ'):
    if len(s) > 3:
        s = s[0]
    pairs = ((eng, NESW[i]) for i,eng in enumerate('NESW'))
    s = reduce(
        lambda s, pair: str.replace(s, *pair),
        pairs,
        s
    )
    return s


def pressure(mbar):
    return '{:.3f}'.format(float(mbar) / 1000).replace('.', ',')


def temperature(x):
    return str(x).replace('-', '&minus;').replace('.', ',')


def hour_minute(x):
    return f'{x["hour"]}:{x["minute"]}'
