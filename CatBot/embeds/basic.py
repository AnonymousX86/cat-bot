# -*- coding: utf-8 -*-
from typing import Dict

from discord import Member

from CatBot.embeds.core import BlueEmbed, GreenEmbed
from CatBot.settings import bot_version, bot_stage


class InfoEmbed(BlueEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ':information_source: Informacje'
        self.add_field(
            name='Wersja',
            value=f'`{bot_version()}`'
        ).add_field(
            name='Środowisko',
            value=f'`{bot_stage()}`'
        )


class SpotifyEmbed(GreenEmbed):
    def __init__(self, track: Dict, member: Member, **kwargs):
        super().__init__(**kwargs)
        name = track['name']
        artists = list(map(lambda x: x['name'], track['artists']))
        self.add_field(
            name=name,
            value=f'**{", ".join(artists)}**\n'
                  f'[ [Spotify]({track["external_urls"]["spotify"]}) ]'
        ).set_thumbnail(
            url=track['album']['images'][0]['url']
        ).set_author(
            name=f'{member.display_name} udostępnił(a):',
            icon_url=member.avatar_url
        )
