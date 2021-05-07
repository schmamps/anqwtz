"""view lister"""
import re
import typing

from ...lib import data
from .defs import View


def get_default(view_list: typing.List[View]) -> int:
    for i, v in enumerate(view_list):
        if v.param == '':
            return i

    return 0


def get_overlay(view: dict) -> View:
    short = re.sub(r'[^a-z]+', '', view.get('title', '').lower())
    param = view.get('param', short)
    src = view.get('src', short)

    return View(param, src)


def list_group(overlays: typing.List[dict]) -> typing.List[View]:
    return [get_overlay(over) for over in overlays]


def list_all() -> typing.List[View]:
    all = [
        get_overlay(view)
        for view
        in data.load('overlays')['overlays']
    ]

    return all
