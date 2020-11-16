# -*- coding: utf-8 -*-
from socket import gethostname, gethostbyname

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
        value='```md\n'
              ' vmi472388.contaboserver.net\n'
              '-----------------------------\n'
              '```W razie problemów, napisz do Anona.\n'
              'Zobacz też [stronę internetową](https://vmi472388.contaboserver.net/ "Qba Server").',
        inline=False
    ).add_field(
        name='Status',
        value='Online' if status else f'Offline \u2015 {error}'
    ).add_field(
        name='Gracze online',
        value='{0.online}/{0.max}'.format(status.players) if status else '\u2013'
    ).add_field(
        name='Ping',
        value='{}ms'.format(int(round(status.latency, 0)) if status else "\u2013 ")
    ).add_field(
        name='Pobieranie',
        value='Wszystkie pliki sa dostępne na'
              ' [stronie internetowej](https://vmi472388.contaboserver.net/ "Qba Server").',
        inline=False
    ).add_field(
        name='Forge 1.12',
        value='Wersja: 14.23.5.2854\n'
              '[Pobierz](https://files.minecraftforge.net/maven/net/minecraftforge/forge/1.12.2-14.23.5.2854/'
              'forge-1.12.2-14.23.5.2854-installer.jar "Minecraft Forge") 4 MB\n'
              '[mirror](https://vmi472388.contaboserver.net/downloads/forge-1.12.2-14.23.5.2854-installer.jar'
              ' "Qba Server")'
    ).add_field(
        name='Paczka modów',
        value='Wersja: 1.2.0\n'
              '[Pobierz](https://vmi472388.contaboserver.net/downloads/Mody_v1.2.7z "Qba Server") 215 MB\n'
              '[Crystal Launcher](https://vmi472388.contaboserver.net/downloads/Mody_v1.2_CL.clpkg "Qba Server")'
              ' 236 MB\n'
              'Paczkę stworzył <@221306966834806785>. :hugging:\n'
    ).add_field(
        name='Aktualizacja paczki',
        value='`1.2.0` :arrow_right: `1.2.2`\n'
              '[Pobierz](https://vmi472388.contaboserver.net/downloads/Update_v1.2.0_v1.2.2.7z "Qba Server") 24MB'
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


def ip_em() -> Embed:
    return Embed(
        title=f':information_source: {gethostbyname(gethostname())}',
        color=Color.blurple()
    )
