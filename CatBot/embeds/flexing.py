# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List, Optional

from discord import Embed, Color, User, Member

from CatBot.embeds.core import BaseEmbed, DoneEmbed
from CatBot.utils.database import Flex


class FlexAddedEmbed(DoneEmbed):
    def __init__(self, member: Member, reason: str, **kwargs):
        super().__init__(**kwargs)
        self.title = ':muscle: Flex'
        self.description = f'{member.mention} dostał(a) flexa za:\n\n> {reason}'
        self.set_thumbnail(url=member.avatar_url)


class FlexesEmbed(DoneEmbed):
    def __init__(self, user: User, flexes: List[Flex], **kwargs):
        super().__init__(**kwargs)
        self.title = f':muscle: Flexy: {user.display_name}'
        self.description = 'Ostatnie 10 flexów.'
        self.set_thumbnail(
            url=user.avatar_url
        )
        if not len(flexes):
            self.add_field(
                name='Brak',
                value=f'{user.display_name} nie ma (jeszcze) flexów.'
            )
        else:
            for i, flex in enumerate(flexes):
                self.add_field(
                    name=f'`{"0" if i < 9 else ""}{i + 1}.`'
                         f'  {str(flex.flex_date)}',
                    value=flex.reason.capitalize(),
                    inline=False
                )


class FlextopEmbed(DoneEmbed):
    def __init__(self, users: List[User], counts: List[Flex],
                 days: int, **kwargs):
        super().__init__(**kwargs)
        self.title = ':dart: Topowe flexy'
        self.description = f'Lista najbardziej flexujących się osób z' \
                           f' ostatnich {days} dni.'
        if not (le := len(users)):
            self.add_field(
                name='\u200b',
                value=':x: Brak flexów!'
            )
        else:
            f = (users, counts)
            if le > 0:
                self.add_field(
                    name=':first_place: Pierwsze miejsce',
                    value='{0[0]} \u2015 **{1[0]}**'.format(*f),
                    inline=False
                )
            if le > 1:
                if counts[1] == counts[0]:
                    title = ':first_place: Egzekwo'
                else:
                    title = ':second_place: Drugie miejsce'
                self.add_field(
                    name=title,
                    value='{0[1]} \u2015 **{1[1]}**'.format(*f),
                    inline=False
                )
            if le > 2:
                if counts[2] == counts[0]:
                    title = ':first_place: Egzekwo'
                elif counts[2] == counts[1]:
                    title = ':second_place: Egzekwo'
                else:
                    title = ':third_place: Trzecie miejsce'
                self.add_field(
                    name=title,
                    value='{0[2]} \u2015 **{1[2]}**'.format(*f),
                    inline=False
                )
