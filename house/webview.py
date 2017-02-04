from copy import deepcopy
from math import ceil
from time import localtime
from typing import Tuple
from . import weather, rasp
from .config import config


class HTMLStrings:
    SPACE = '<span style="padding-left:1em;"></span>'

    def __init__(self) -> None:
        self.w = weather.Weather(**config['weather'])
        self.r = rasp.Rasp(**config['rasp'])
        for k, v in config['web'].items():
            setattr(self, k, v)

    def weather_strings(self) -> Tuple[str, ...]:
        try:
            jw = self.w()
            w_now = jw['current_observation']

            temp_now = weather.temperature(w_now['temp_c'])
            temp_feels_now = weather.temperature(w_now['feelslike_c'])
            wind_now = weather.wind(w_now['wind_kph'])
            wind_dir_now = weather.wind_dir(w_now['wind_dir'])
            rel_hum_now = w_now['relative_humidity']
            pres_now = weather.pressure(w_now['pressure_mb'])
            cond_now = w_now['weather']
            str_now = f'{cond_now}{self.SPACE} {temp_now}&nbsp;&deg;C&nbsp;({temp_feels_now}&nbsp;&deg;C){self.SPACE} {rel_hum_now}{self.SPACE} {wind_dir_now}&nbsp;{wind_now}&nbsp;м/с{self.SPACE} {pres_now}&nbsp;бар'

            w_astro = jw['moon_phase']
            moon_phase = w_astro['phaseofMoon']
            sunrise = weather.hour_minute(w_astro['sunrise'])
            sunset = weather.hour_minute(w_astro['sunset'])
            str_astro = f'{moon_phase}. Солнце на небе c {sunrise} до {sunset}'

            if localtime().tm_hour < 19:
                w_day = jw['forecast']['simpleforecast']['forecastday'][0]
                day = 'Сегодня'
            else:
                w_day = jw['forecast']['simpleforecast']['forecastday'][1]
                day = 'Завтра'
            low_day = weather.temperature(w_day['low']['celsius'])
            high_day = weather.temperature(w_day['high']['celsius'])
            max_wind_day = weather.wind(w_day['maxwind']['kph'])
            max_wind_dir_day = weather.wind_dir(w_day['maxwind']['dir'])
            qpf_day = weather.precipitation(w_day['qpf_allday']['mm'])
            cond_day = w_day['conditions'].lower()
            str_day = f'{day} {cond_day}, {qpf_day}&nbsp;мм, от {low_day}&nbsp;&deg;C до {high_day}&nbsp;&deg;C и {max_wind_dir_day} ветер до {max_wind_day}&nbsp;м/с'
        except KeyError:
            return 'Информация о погоде недоступна',
        except Exception as e:
            return f'Exception of type {type(e)}: {e}',
        return str_now, str_astro, str_day

    def rasp_strings(self) -> Tuple[str, ...]:
        try:
            jr = self.r()
            rt_orig = rasp.RaspThreads(deepcopy(jr['threads']))
            rt = deepcopy(rt_orig).after(self.runtime_to_station).before(self.rasp_time_interval)
            if len(rt) < self.rasp_min_count:
                rt.extend(rt_orig.after(self.rasp_time_interval)[:self.rasp_min_count - len(rt)])
            threads = []
            for x in rt:
                hm = x['departure_datetime'].strftime('%H:%M')
                minutes = ceil((x['departure_datetime'] - rt.now).seconds / 60)
                title = x['thread']['title'][0]
                thread = f'{title}&nbsp;{hm}&nbsp;({minutes})'
                if not self.r.have_a_stop_at(x['thread']['uid']):
                    thread = f'<i>{thread}</i>'
                threads.append(thread)
            str_threads = f'{self.SPACE} '.join(threads)
            return str_threads,
        except KeyError as e:
            return f'Информация о расписании недоступна {e}',