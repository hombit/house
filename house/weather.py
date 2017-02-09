import requests
from functools import reduce
from numbers import Real
from typing import Optional, SupportsFloat, Tuple, Union
from urllib.parse import urljoin
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


def precipitation(x: Union[Real, str]) -> str:
    return str(x).replace('.', ',')


def pressure(mbar: SupportsFloat) -> str:
    return str(float(mbar) - 1000).replace('-', '&minus;').replace('.', ',')


def temperature(x: Union[Real, str]) -> str:
    return str(x).replace('-', '&minus;').replace('.', ',')


def hour_minute(x: dict) -> str:
    return f'{x["hour"]}:{x["minute"]}'
