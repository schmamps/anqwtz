"""URL Class"""
from collections import OrderedDict
from urllib import parse

from flask import Request


SCHEME_TABLE = {
    'http': 80,
    'https': 443,
    'ftp': 21,
}


def compare_eq(a, b):
    return str(a) == str(b)


class Url(object):
    path: str = ''
    query: dict = {}

    def __init__(self, url: str):
        parsed = parse.urlparse(url)

        self.path = parsed.path
        self.query = parse.parse_qs(parsed.query)

    @property
    def query_string(self):
        query = OrderedDict()
        keys = [key for key in self.query.keys() if self.query[key]]

        for key in reversed(sorted(keys)):
            query[key] = self.query[key]

        return parse.urlencode(query, doseq=True)

    @staticmethod
    def from_request(req: Request):
        self = Url(req.path)
        self.query = {
            key: val
            for key, val
            in req.args.items()
        }

        return self

    def __str__(self):
        return '?'.join([
            comp
            for comp
            in [self.path, self.query_string]
            if comp
        ])

    def __eq__(self, other):
        return compare_eq(self, other)

    def __ne__(self, other):
        return not compare_eq(self, other)
