import json, os, sys


CONFIG_FILE_PATH = os.path.join(sys.prefix, 'house/config/house.json')


with open(CONFIG_FILE_PATH, 'r') as fd:
    config = json.load(fd)

__module = sys.modules[__name__]

for k, v in config.items():
    setattr(__module, k, v)