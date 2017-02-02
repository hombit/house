import requests
from urllib.parse import urljoin
from functools import reduce
from typing import Optional, SupportsFloat, Tuple, Union
from .secrets import weather_underground_api_key
from .tools import ApiBasic


_base_url = 'https://api.wunderground.com/api/'


class Weather(ApiBasic):
    @staticmethod
    def _get(location: str,
            lang: Optional[str],
            features: Tuple[str, ...] = ('conditions', 'forecast', 'astronomy')
        ) -> dict:
        if lang is None:
            lang = 'EN'
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


def wind(mph: SupportsFloat) -> str:
    return '{:.1f}'.format(float(mph) / 3.6).replace('.', ',')


def wind_dir(s: str, nesw: str = 'СВЮЗ') -> str:
    if len(s) > 3:
        s = s[0]
    pairs = ((eng, nesw[i]) for i, eng in enumerate('NESW'))
    s = reduce(
        lambda x, pair: str.replace(x, *pair),
        pairs,
        s
    )
    return s


def precipitation(x: Union[int, float, str]) -> str:
    return str(x).replace('.', ',')


def pressure(mbar: SupportsFloat) -> str:
    return '{:.3f}'.format(float(mbar) / 1000).replace('.', ',')


def temperature(x: Union[int, float, str]) -> str:
    return str(x).replace('-', '&minus;').replace('.', ',')


def hour_minute(x: dict) -> str:
    return f'{x["hour"]}:{x["minute"]}'
