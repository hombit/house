import copy
import datetime
import requests
from collections import UserList
from operator import lt, ge
from typing import Any, Callable, Optional, TypeVar, Union
from urllib.parse import urljoin
from .tools import ApiBasic
from .secrets import yandex_api_key


T = TypeVar('T')


_base_url = 'https://api.rasp.yandex.net/v1.0/search/'


def _days_after_today(x: int = 0) -> str:
    today = datetime.date.today()
    day = today + datetime.timedelta(days=x)
    return day.strftime('%Y-%m-%d')


def _datetime_fromstring(s: str) -> datetime.datetime:
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


class RaspThreads(UserList):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for x in self:
            for key in ('arrival', 'departure'):
                x[f'{key}_datetime'] = _datetime_fromstring(x[key])
        self.sort(key=lambda x: x['departure_datetime'])
        self._now = datetime.datetime.now()

    @property
    def now(self) -> datetime.datetime:
        return copy.copy(self._now)

    def _filter_before_after(self: T,
                             operator: Callable[[Any, Any], bool],
                             seconds_from_now: Union[int, float]) -> T:
        t = self._now + datetime.timedelta(seconds=seconds_from_now)
        self.data = list(filter(
            lambda x: operator(x['departure_datetime'], t),
            self
        ))
        return self

    def after(self: T, *args, **kwargs) -> T:
        return self._filter_before_after(ge, *args, **kwargs)

    def before(self: T, *args, **kwargs) -> T:
        return self._filter_before_after(lt, *args, **kwargs)


class Rasp(ApiBasic):
    @staticmethod
    def _get(from_station: str,
             to_station: str,
             lang: str,
             system: str,
             transport_types: str,
             date: Optional[str] = None) -> dict:
        if date is None or date == 'today':
            date = _days_after_today(0)
        if date == 'tomorrow':
            date = _days_after_today(1)
        query_tuple = (
            f'apikey={yandex_api_key}',
             'format=json',
            f'from={from_station}',
            f'to={to_station}',
            f'lang={lang}',
            f'date={date}',
            f'system={system}',
            f'transport_types={transport_types}',
        )
        query = '?' + '&'.join(query_tuple)
        url = urljoin(_base_url, query)
        r = requests.get(url)
        return r.json()
