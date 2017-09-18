import copy
import datetime
import requests
from collections import UserList
from inspect import getfullargspec
from operator import lt, ge
from typing import Any, Callable, Optional, TypeVar, Union
from urllib.parse import urljoin
from .tools import ApiBasic
from .secrets import yandex_api_key


T = TypeVar('T')


_base_url = 'https://api.rasp.yandex.net/v1.0/'


_base_query_params = {'apikey': yandex_api_key,
                      'format': 'json',}


def _days_after_today(x: int = 0) -> str:
    today = datetime.date.today()
    day = today + datetime.timedelta(days=x)
    return day.strftime('%Y-%m-%d')


def _datetime_fromstring(s: str) -> datetime.datetime:
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


def _optional_date_conversation(date: str) -> str:
    if date is None or date == 'today':
        return _days_after_today(0)
    if date == 'tomorrow':
        return _days_after_today(1)
    return date


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_thread_info = self._cache_decorator(self._get_thread_info)

    @staticmethod
    def _get(from_station: str,
             to_station: str,
             lang: str,
             system: str,
             transport_types: str,
             date: Optional[str] = None,
             **kwargs) -> dict:
        date = _optional_date_conversation(date)
        query_params = {'from': from_station,
                        'to': to_station,
                        'lang': lang,
                        'date': date,
                        'system': system,
                        'transport_types': transport_types,}
        query_params.update(_base_query_params)
        url = urljoin(_base_url, 'search/')
        r = requests.get(url, params=query_params)
        return r.json()

    @staticmethod
    def _get_thread_info(thread_uid: str,
                         lang: str,
                         system: str,
                         date: Optional[str] = None) -> dict:
        date = _optional_date_conversation(date)
        query_params = {'uid': thread_uid,
                        'lang': lang,
                        'date': date,
                        'show_systems': system,}
        query_params.update(_base_query_params)
        url = urljoin(_base_url, 'thread/')
        r = requests.get(url, params=query_params)
        return r.json()

    def thread_info(self,
                    thread_uid: str,
                    date: Optional[str] = None) -> dict:
        kwargs = {'thread_uid':thread_uid, 'date':date}
        for k in getfullargspec(self._get_thread_info).args:
            if k not in kwargs:
                kwargs[k] = self._call_kwargs[k]
        return self.get_thread_info(**kwargs)

    def have_a_stop_at(self,
                       thread_uid: str,
                       date: Optional[str] = None) -> bool:
        system = self._call_kwargs['system']
        stop_station = self._call_kwargs['stop_station']
        stops = self.thread_info(thread_uid, date)['stops']
        for stop in stops:
            st = stop['station']
            if 'codes' not in st:  # Work around bug in Yandex.Rasp API
                continue
            if st['codes'][system] == stop_station:
                stop_time = stop['stop_time'] or 0
                return int(stop_time) > 0
        return False
