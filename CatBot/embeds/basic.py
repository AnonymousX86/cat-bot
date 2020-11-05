# -*- coding: utf-8 -*-
from discord import Embed, Color

from CatBot.data import archives, server_status
from settings import Settings


def please_wait_em() -> Embed:
    return Embed(
        title=':hourglass_flowing_sand: Daj mi chwilę...',
        color=Color.blurple()
    )


def info_em() -> Embed:
    return Embed(
        title=':information_source: Informacje',
        color=Color.blurple()
    ).add_field(
        name='Wersja',
        value=f'{Settings().bot_version}'
    )


def mc_embed() -> Embed:
    status, error = server_status()
    em = Embed(
        title=':pick: Minecraft',
        color=Color.blurple()
    ).add_field(
        name='Adres',
        value='```\nkociaki.tasrv.com\n```W razie problemów, napisz do Anona.',
        inline=False
    ).add_field(
        name='Silnik',
        value='```\nForge  1.12.2  14.23.5.2854\n```'
              '[Pobierz](http://www.mediafire.com/file/tazj0l79mbtudq5/forge-1.12.2-14.23.5.2854-installer.jar/file)'
    ).add_field(
        name='Paczka modów',
        value='```\nWersja 1, by: Mixiu\n```'
              '[Pobierz](https://drive.google.com/folderview?id=1JKbpJaInv_dUCbUxD7Wj8oqrdSYnLl6q)'
    ).add_field(
        name='Status',
        value='Online' if status else f'Offline \u2015 {error}',
        inline=False
    ).add_field(
        name='Gracze online',
        value='{0.online}/{0.max}'.format(status.players) if status else '\u2013'
    ).add_field(
        name='Ping',
        value='{}ms'.format(int(round(status.latency, 0)) if status else "\u2013 ")
    )
    return em


def archives_embed() -> Embed:
    em = Embed(
        title=':inbox_tray: Archiwa',
        color=Color.blurple()
    )
    for a in archives():
        em.add_field(
            name=f'{a.name}',
            value=f'[Pobierz]({a.link}) - {a.size}'
        )
    return em
