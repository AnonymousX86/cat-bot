# -*- coding: utf-8 -*-
from socket import gethostname, gethostbyname
from typing import Dict

from discord import Embed, Color, Member

from CatBot.data import archives, server_status
from settings import Settings


def please_wait_em() -> Embed:
    return Embed(
        title=':hourglass_flowing_sand: Daj mi chwilę...',
        color=Color.blurple()
    )


def done_em(description: str = '') -> Embed:
    return Embed(
        title=':white_check_mark: Gotowe',
        description=description,
        color=Color.blurple()
    )


def missing_perms_em() -> Embed:
    return Embed(
        title=':x: Nie możesz tego zrobić',
        description='Prawdopodobnie nie posiadasz odpowiednich uprawnień.',
        color=Color.blurple()
    )


def missing_user_em() -> Embed:
    return Embed(
        title=':x: Nie podałeś(aś) użytkownika',
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


def skryba_em() -> Embed:
    return Embed(
        title=':scroll: Skryba kiedyś powiedział...',
        description='*Moim zdaniem to nie ma tak, że dobrze albo że nie dobrze. Gdybym miał powiedzieć, co cenię w'
                    ' życiu najbardziej, powiedziałbym, że ludzi. Ekhm... Ludzi, którzy podali mi pomocną dłoń, kiedy'
                    ' sobie nie radziłem, kiedy byłem sam. I co ciekawe, to właśnie przypadkowe spotkania wpływają na'
                    ' nasze życie. Chodzi o to, że kiedy wyznaje się pewne wartości, nawet pozornie uniwersalne, bywa,'
                    ' że nie znajduje się zrozumienia, które by tak rzec, które pomaga się nam rozwijać. Ja miałem'
                    ' szczęście, by tak rzec, ponieważ je znalazłem. I dziękuję życiu. Dziękuję mu, życie to śpiew,'
                    ' życie to taniec, życie to miłość. Wielu ludzi pyta mnie o to samo, ale jak ty to robisz?, skąd'
                    ' czerpiesz tę radość? A ja odpowiadam, że to proste, to umiłowanie życia, to właśnie ono sprawia,'
                    ' że dzisiaj na przykład buduję maszyny, a jutro... kto wie, dlaczego by nie, oddam się pracy'
                    ' społecznej i będę ot, choćby sadzić... znaczy... marchew.*',
        color=Color.blurple()
    )


def spotify_em(track: Dict, member: Member) -> Embed:
    name = track['name']
    artists = map(lambda x: x['name'], track['artists'])
    return Embed(
        color=Color.green()
    ).add_field(
        name='Tytuł',
        value=name,
        inline=False
    ).add_field(
        name='Wykonawca(y)',
        value=', '.join(artists),
        inline=False
    ).add_field(
        name='Spotify',
        value=track['external_urls']['spotify'],
        inline=False
    ).set_thumbnail(
        url=track['album']['images'][-1]['url']
    ).set_author(
        name=f'{member.display_name} udostępnił(a):',
        icon_url=member.avatar_url
    )
