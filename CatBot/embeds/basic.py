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
        value='```\nvmi472388.contaboserver.net\n```W razie problemów, napisz do Anona.',
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
        name='Silnik',
        value='```\nForge  1.12.2  14.23.5.2854\n```'
              '[Pobierz](https://files.minecraftforge.net/maven/net/minecraftforge/forge/1.12.2-14.23.5.2854/'
              'forge-1.12.2-14.23.5.2854-installer.jar "Minecraft Forge"), [mirror]'
              '(https://mega.nz/file/oEVnnKzD#8RpVgeTXuFa7H-WxwTAzUlIF_qjAQ385c4bDMvpzjag  "MEGA")',
        inline=False
    ).add_field(
        name='Paczki modów (by: Mixiu)',
        value='**v1.1** \u2015'
              ' [Pobierz](https://mega.nz/file/IUMxQQYb#tSwPOmNV72v_CC2vMP0BT7qXWY_ijCvLbxly-m_Wpn4 "MEGA"),'
              ' [Crystal Launcher](https://mega.nz/file/pYdHkapa#hNPERAJITNkGNtQ-TqzNFlDnNff-y3IhBWzFn2ktq6Q "MEGA")\n'
              '**v1.1 lite** \u2015'
              ' [Pobierz](https://mega.nz/file/5FdxEYID#oZK_Vyen6xcDE_KfikHjhSLVr1p_DYma8PYEHs-zKE0 "MEGA"),'
              ' [Crystal Launcher](https://mega.nz/file/scFBAaTa#Mxo1QljM6UZA-UPw382s6vhysYF9D6H2tAJ9NE2udBk "MEGA")'
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
