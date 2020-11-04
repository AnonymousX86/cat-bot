# -*- coding: utf-8 -*-
from discord import Embed, Color

from settings import Settings


def info_em():
    return Embed(
        title=':information_source: Informacje',
        color=Color.blurple()
    ).add_field(
        name='Wersja',
        value=f'{Settings().bot_version}'
    )


def mc_embed():
    return Embed(
        title=':pick: Minecraft',
        color=Color.blurple()
    ).add_field(
        name='Adres',
        value='`kociaki.tasrv.com`'
    ).add_field(
        name='Wersja',
        value='1.12.2 Forge - [pobierz]()'
    ).add_field(
        name='Paczka modów',
        value='[Pobierz]()'
    )
