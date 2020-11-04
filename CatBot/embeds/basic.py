# -*- coding: utf-8 -*-
from discord import Embed, Color

from CatBot.data import archives
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
        value='```\nkociaki.tasrv.com\n```W razie problemów, napisz do Anona.',
        inline=False
    ).add_field(
        name='Silnik',
        value='```\nForge 1.12.2 14.23.5.2854\n```'
              '[Pobierz](http://www.mediafire.com/file/tazj0l79mbtudq5/forge-1.12.2-14.23.5.2854-installer.jar/file)'
    ).add_field(
        name='Paczka modów',
        value='```\nWersja 1, by: Mixiu\n```'
              '[Pobierz](https://drive.google.com/folderview?id=1JKbpJaInv_dUCbUxD7Wj8oqrdSYnLl6q)'
    )


def archives_embed():
    em = Embed(
        title=':inbox_tray: Archiwa',
        color=Color.blurple()
    )
    for a in archives:
        em.add_field(
            name=f'{a.name}',
            value=f'[Pobierz]({a.link}) - {a.size}'
        )
    return em
