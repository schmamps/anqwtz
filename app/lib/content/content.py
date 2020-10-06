"""Content Generator"""
import math
import urllib.parse
import random
import re
import typing

import arrow
import faker
import inflect

from . import reference


def get_date(
    page_id: int,
    rel_id: int,
    rel_date: arrow
) -> str:
    """Get correct date for `page_id` relative to `rel_id` and `rel_date`

    Args:
        page_id (int): id of requested comic
        rel_id (int): relative ID
        rel_date (tuple): relative date (Ymd) for rel_id

    Returns:
        str: e.g. "July 29th, 2020"
    """
    id_inc = math.floor(7.0 / 3.0 * (page_id - rel_id))
    day_inc = -1 if id_inc < 0 else 1
    date = arrow.get(rel_date).shift(days=id_inc)

    while date.weekday() not in (0, 2, 4):
        date = date.shift(days=day_inc)

    return date.format('MMMM Do, YYYY')


def get_id_date(page_id: int):
    return get_date(page_id, reference.id, reference.date)


def create_name(name: typing.Callable) -> typing.Tuple[str, str]:
    comps = []  # type: typing.List[str]

    while len(comps) != 2:
        full_name = name()
        comps = full_name.split(' ')

    return str(comps[0]), str(comps[1])


def format_paragraph(para: str, vars) -> str:
    clean = re.sub(r'\s+', ' ', para).strip()

    return clean.format(*vars)


def create_panel(paras: typing.List[str], vars: typing.List[typing.Any]):
    return '\n\n'.join([format_paragraph(para, vars) for para in paras])


def pedant(word: str, suffocate=str):
    base = word[:int(len(word) * .667)]
    suffix = word[len(base):]

    return base + suffocate(suffix).upper()


def create_var(initial: str, create: typing.Callable):
    converted = create(initial)

    return converted if converted else initial


def compound(root: str, suffix: str):
    if root.endswith(suffix[0]):
        return root[:-1] + suffix

    return root + suffix


def panels(seed: typing.Any) -> typing.List[str]:
    eng = inflect.engine()
    faker.Faker.seed(seed if isinstance(seed, (str, int)) else str(seed))
    fake = faker.Faker(['en_CA'])

    angola, maldives = create_name(fake.name)
    mixed_drinks = create_var(' '.join(fake.words(2)), eng.plural_noun)
    food = create_var(fake.word(), eng.singular_noun)
    streak = create_var(fake.word(), eng.singular_noun)
    light = create_var(fake.word(), eng.singular_noun)
    meteor = create_var(fake.word(), eng.singular_noun)
    meteoroid = compound(meteor, 'OID')
    meteorites = compound(meteor, 'ITES')
    asteroids = compound(create_var(fake.word(), eng.singular_noun), 'oids')

    panels = [
        # panel 1
        '''
{0}, the sexy
super spy I invented, was
yet again on a mission to
save the world!



Oh no,
you guys!
'''.format(' '.join((angola, maldives))),
        # panel 2
        '''
An evil
mastermind is
planning to
smash {0}
into the
planet!!
'''.format(eng.plural_noun(meteor)),
        # panel 3
        '''
"Ah, then there's nothing to worry about,"
{0} said while consuming stuff associated
with being really cool like {1}
that are hard to make and {2} that's very
                        expensive and doesn't taste
                        as good as a Big Mac
                        anyway, "as a {3} is
                        defined only as the visible
                        {4} of {5} caused by
                        a {6} travelling in
                        the atmosphere. Some {5}
                        hitting our planet
                        won't hurt anyone, yo.
'''.format(angola, mixed_drinks, food, meteor, streak, light, meteoroid),
        # panel 4
        '''
"I think he actually
meant {0} then!!"
shouted {1}'s boss!

       "Again, no
       worries."
       said
       {1}.
'''.format(meteoroid, angola),
        # panel 5
        '''
Most {0} break up inside
atmosphere. It's only {1}
that ever reach the ground, and the
vast majority of those are no larger
than a grain of rice.

                   "Okay. Weird.
                   I guess I'm
                   thinking
                   about
                   {2}?"
                   said the boss.


                        "Correct,"
                        said {3}.
'''.format(meteoroid + 'S', meteorites, asteroids, angola),
        # panel 6
        '''

    THE END









                    {0}
                    {1}
                    WILL RETURN
'''.format(angola.upper(), maldives.upper())
    ]

    return [panel[1:-1] for panel in panels]


def index(page_id: int) -> dict:
    faker.Faker.seed(page_id + 1)
    fake = faker.Faker(['en_CA'])

    page = {}  # type: dict
    page['date'] = get_id_date(page_id)
    page['title'] = fake.paragraph()
    page['contact'] = urllib.parse.quote(fake.paragraph())  # noqa
    page['rss'] = fake.paragraph()
    page['blog'] = [fake.paragraph() for _ in range(random.randint(1, 4))]

    return page
