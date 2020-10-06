"""index page"""
import math
import typing

import arrow
from flask import redirect, render_template, request

from ...lib import content, urly
from . import defs, views


def get_default_id():
    delta = arrow.now() - content.reference.date

    return math.floor(delta.days / 7.0 * 3.0) + content.reference.id


def get_view_data(
    query: str
) -> typing.Tuple[typing.List[defs.View], int]:
    view_list = views.list_all()
    valid_queries = [v.param for v in view_list]

    try:
        return view_list, valid_queries.index(query)
    except ValueError:
        pass

    return view_list, views.get_default(view_list)


def get_page_id_spec(query) -> typing.Optional[int]:
    try:
        return int(query)
    except (TypeError, ValueError):
        return None


def get_comic_data(
    query: str,
    view: defs.View
) -> typing.Tuple[int, urly.Url]:
    url = urly.Url('/index.php')
    url.query[defs.BIWRBR] = view.param

    id_spec = get_page_id_spec(query)
    if id_spec is not None:
        url.query['comic'] = abs(id_spec)

    return id_spec or get_default_id(), url


def get_canons(
    page_id: int
) -> typing.List[str]:
    formatter = '/comics/comic2-{0}{1}.png'

    return [formatter.format(page_id, mod) for mod in ['-2', '']]


def get_page_base(page_id: int, view: views.View) -> dict:
    canons = get_canons(page_id)
    base = {
        'id': page_id,
        'dubs': page_id - (page_id % 100 % 11),
        'canon': canons[1],
        'src': canons
    }

    if view.src and page_id != base['dubs']:
        base['src'] = ['', '/{0}.png'.format(view.src)]

    return base


def get_page_nav(
    relative_url: urly.Url,
    page_id: int,
) -> typing.Dict[str, str]:
    nav = urly.Url(str(relative_url))

    nav.query['comic'] = page_id - 1
    prev = str(nav)

    nav.query['comic'] = page_id + 1
    next = str(nav)

    return {'prev': prev, 'next': next}


def serve_page(page_id: int, url: urly.Url, view: views.View):
    return render_template(
        'index.j2',
        page=get_page_base(page_id, view),
        nav=get_page_nav(url, page_id),
        content=content.index(page_id)
    )


def php(name: str):
    url_spec = urly.Url.from_request(request)
    url_spec.query = dict(request.args)

    view_list, view_idx = get_view_data(url_spec.query.get(defs.BIWRBR, ''))
    page_id, url_actual = get_comic_data(
        url_spec.query.get('comic', ''),
        view_list[view_idx]
    )

    if len(url_spec.path) > 1 and url_spec != url_actual:
        return redirect(str(url_actual), 302)

    return serve_page(page_id, url_actual, view_list[view_idx])
