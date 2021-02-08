# -*- coding: utf-8 -*-
from typing import Dict

from discord import Embed, Color, Member

from CatBot.embeds.custom_classes import ErrorEmbed, SuccessEmbed, BaseEmbed
from CatBot.settings import bot_version, bot_stage


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


def done_em(description: str = '') -> Embed:
    return SuccessEmbed(
        title=':white_check_mark: Gotowe',
        description=description
    )


def please_wait_em() -> Embed:
    return BaseEmbed(
        title=':hourglass_flowing_sand: Daj mi chwilę...',
        color=Color.gold()
    )


def info_em() -> Embed:
    return BaseEmbed(
        title=':information_source: Informacje'
    ).add_field(
        name='Wersja',
        value=f'`{bot_version()}`'
    ).add_field(
        name='Środowisko',
        value=f'`{bot_stage()}`'
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
        url=track['album']['images'][0]['url']
    ).set_author(
        name=f'{member.display_name} udostępnił(a):',
        icon_url=member.avatar_url
    )
