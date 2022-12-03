# -*- coding: utf-8 -*-
from typing import Dict

from discord import Member, Role

from CatBot.embeds.core import BlueEmbed, GreenEmbed, DoneEmbed
from CatBot.settings import bot_version, bot_stage


class AutoroleEmbed(BlueEmbed):
    def __init__(
            self,
            member: Member,
            normal_role: Role,
            guest_role: Role,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.title = ':busts_in_silhouette: Kto to?'
        self.description = f'Czy dać {member.mention} rolę {normal_role.mention}?\n' \
                           f'Jeśli nie, wtedy otrzyma rolę {guest_role.mention}.'


class RoleAddedEmbed(DoneEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = 'Dodano rolę.'


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
