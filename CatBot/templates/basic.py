# -*- coding: utf-8 -*-
from random import randint

from discord import Embed, Color

from settings import Settings


def please_wait_em():
    return Embed(
        title=f'Czekaj...',
        color=Color.blurple()
    )


def cat_img_em(sub_name: str, sub_url: str):
    return Embed(
        title=f':cat2: Kotek',
        description=f'[/r/{sub_name}]({sub_url})',
        color=Color.blurple()
    ).set_image(
        url=sub_url
    )


def catfact_em(fact: str):
    return Embed(
        title=':cat2: Catfact',
        description=fact,
        color=Color.blurple()
    )


def info_em():
    return Embed(
        title=':information_source: Informacje',
        color=Color.blurple()
    ).add_field(
        name='Wersja',
        value=f'{Settings().bot_version}'
    )


def coin_em():
    result = [':small_red_triangle: Orzeł', ':small_red_triangle_down: Reszka']
    return Embed(
        title=result[randint(0, 1)],
        color=Color.blurple()
    )
