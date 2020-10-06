"""serve images"""
import io
from pathlib import Path
from typing import Any

from flask import make_response
from PIL import Image, ImageDraw, ImageFont

from ...lib import content, data


CWD = Path(__file__).parent


def is_list(val: Any) -> bool:
    return type(val) == list


def get_by_name(name) -> dict:
    images = data.load('images')

    nom = {'content': name}
    nom.update(images.get('.', {}))
    nom.update(images.get(name, {}))

    cfg = {}
    for key in dict.keys(nom):
        cfg[key] = tuple(nom[key]) if is_list(nom[key]) else nom[key]

    return cfg


def get_font(cfg: dict) -> ImageFont:
    font_path = str(cfg.get('font_path', CWD.joinpath('./luximr.ttf')))
    font_size = cfg.get('font_size', 24)

    return ImageFont.truetype(font_path, font_size)


def get_overlay(base: Image, color: tuple) -> Image:
    text = Image.new(base.mode, base.size, color)
    draw = ImageDraw.Draw(text)

    return text, draw


def respond(img: Image.Image):
    byteArr = io.BytesIO()
    img.save(byteArr, format='PNG')

    response = make_response(byteArr.getvalue())
    response.headers.set('Content-Type', 'image/png')

    return response


def comic(name: str):
    cfg = get_by_name(name)

    with open(str(CWD.joinpath('comic.png')), 'rb') as src:
        comic = Image.open(src).convert(mode='RGBA')
        text, draw = get_overlay(comic, (0, 0, 0, 0))
        font = get_font({'font_size': 10})
        POS = [
            (10, 10), (250, 10), (380, 10),
            (10, 250), (200, 250), (500, 250)]

        for idx, panel in enumerate(content.panels(name)):
            draw.text(
                POS[idx],
                panel,
                font=font,
                fill=cfg['fg'],
                spacing=3)

    return respond(Image.alpha_composite(comic, text))


def png(name: str):
    cfg = get_by_name(name)

    base = Image.new('RGBA', cfg['img_size'], cfg['bg'])
    text, draw = get_overlay(base, (0, 0, 0, 0))
    font = get_font(cfg)
    draw.text(cfg['xy'], cfg['content'], font=font, fill=cfg['fg'])

    return respond(Image.alpha_composite(base, text))
