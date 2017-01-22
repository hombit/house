import json
import os


_default_secrets_filename = 'secrets.json'

_search_paths = (
    './',
    os.path.join(os.environ.get('HOME', '/root'), '.config/house/'),
    '/etc/house/',
)


def _get_json():
    for path in _search_paths:
        filename = os.path.join(path, _default_secrets_filename)
        try:
            with open(filename, 'r') as fp:
                return json.load(fp)
        except FileNotFoundError:
            pass
    raise FileNotFoundError('Cannot find secrets.json file')

_json_ = _get_json()
yandex_api_key = _json_['yandex_api_key']
weather_underground_api_key = _json_['weather_underground_api_key']
