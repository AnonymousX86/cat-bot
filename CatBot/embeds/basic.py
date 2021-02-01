# -*- coding: utf-8 -*-
from datetime import datetime as d
from socket import gethostname, gethostbyname
from typing import Dict, List

from discord import Embed, Color, Member, User

from CatBot.settings import Settings
from CatBot.utils.database import Flex


class BaseEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.timestamp = kwargs['timestamp']
        except KeyError:
            self.timestamp = d.utcnow()
        try:
            self.colour = kwargs['color']
        except KeyError:
            self.colour = Color.blurple()


class ErrorEmbed(BaseEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colour = Color.red()


class SuccessEmbed(BaseEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colour = Color.green()


def please_wait_em() -> Embed:
    return BaseEmbed(
        title=':hourglass_flowing_sand: Daj mi chwilę...'
    )


def done_em(description: str = '') -> Embed:
    return SuccessEmbed(
        title=':white_check_mark: Gotowe',
        description=description
    )


def missing_perms_em() -> Embed:
    return ErrorEmbed(
        title=':x: Nie możesz tego zrobić',
        description='Prawdopodobnie nie posiadasz odpowiednich uprawnień.'
    )


def missing_user_em() -> Embed:
    return ErrorEmbed(
        title=':x: Nie podałeś(aś) użytkownika'
    )


def custom_error_em(description: str = 'Nieznany błąd.') -> Embed:
    return ErrorEmbed(
        title=':x: Coś poszło nie tak!',
        description=description
    )


def info_em() -> Embed:
    return BaseEmbed(
        title=':information_source: Informacje'
    ).add_field(
        name='Środowisko',
        value=f'`{Settings().bot_stage}`'
    )


def ip_em() -> Embed:
    return BaseEmbed(
        title=f':information_source: {gethostbyname(gethostname())}'
    )


def skryba_em() -> Embed:
    return BaseEmbed(
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
                    ' społecznej i będę ot, choćby sadzić... znaczy... marchew.*'
    )


def spotify_em(track: Dict, member: Member) -> Embed:
    name = track['name']
    artists = list(map(lambda x: x['name'], track['artists']))
    return BaseEmbed(
        color=Color.dark_green()
    ).add_field(
        name='Tytuł',
        value=name
    ).add_field(
        name='Wykonawca' if len(artists) == 1 else 'Wykonawcy',
        value=', '.join(artists)
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


def user_flexes_em(user: User, flexes: List[Flex]) -> Embed:
    em = BaseEmbed(
        title=f':muscle: Flexy: {user.display_name}',
        description='Ostatnie 10 flexów.'
    ).set_thumbnail(
        url=user.avatar_url
    )
    if not len(flexes):
        em.add_field(
            name='Brak',
            value=f'{user.display_name} nie ma (jeszcze) flexów.'
        )
    for i, flex in enumerate(flexes):
        em.add_field(
            name=f'`{i + 1}.`  {str(flex.flex_date)}',
            value=flex.reason.capitalize(),
            inline=False
        )
    return em


def flextop_em(users: list, counts: list, days: int) -> Embed:
    em = BaseEmbed(
        title=':dart: Topowe flexy',
        description=f'Lista najbardziej flexujących się osób z ostatnich {days} dni.',
        timestamp=d.utcnow(),
        color=Color.blurple()
    )
    le = len(users)
    if not le:
        em.add_field(
            name='\u200b',
            value=':x: Brak flexów!'
        )
    else:
        f = (users[::-1], counts[::-1])
        if le > 0:
            em.add_field(
                name=':first_place: Pierwsze miejsce',
                value='{0[0]} \u2015 **{1[0]}**'.format(*f),
                inline=False
            )
        if le > 1:
            em.add_field(
                name=':second_place: Pierwsze miejsce',
                value='{0[1]} \u2015 **{1[1]}**'.format(*f),
                inline=False
            )
        if le > 2:
            em.add_field(
                name=':third_place: Pierwsze miejsce',
                value='{0[2]} \u2015 **{1[2]}**'.format(*f),
                inline=False
            )
    return em
