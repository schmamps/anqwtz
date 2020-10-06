"""JSON utility"""
import json
from pathlib import Path


APP_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = 'data'


def get_filename(name: str) -> str:
    return '{0}.json'.format(name)


def get_data_path(name: str) -> Path:
    return APP_ROOT.joinpath(DATA_DIR).joinpath(get_filename(name))


def load_json(name):
    full_path = get_data_path(name)

    with open(full_path) as file:
        return json.loads(file.read())
