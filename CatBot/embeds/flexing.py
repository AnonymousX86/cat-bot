# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List

from discord import Embed, Color, User

from CatBot.embeds.custom_classes import BaseEmbed
from CatBot.utils.database import Flex


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
            name=f'`{"0" if i < 9 else ""}{i + 1}.`  {str(flex.flex_date)}',
            value=flex.reason.capitalize(),
            inline=False
        )
    return em


def flextop_em(users: list, counts: list, days: int) -> Embed:
    em = BaseEmbed(
        title=':dart: Topowe flexy',
        description=f'Lista najbardziej flexujących się osób z ostatnich'
                    f' {days} dni.',
        timestamp=datetime.utcnow(),
        color=Color.blurple()
    )
    le = len(users)
    if not le:
        em.add_field(
            name='\u200b',
            value=':x: Brak flexów!'
        )
    else:
        f = (users, counts)
        if le > 0:
            em.add_field(
                name=':first_place: Pierwsze miejsce',
                value='{0[0]} \u2015 **{1[0]}**'.format(*f),
                inline=False
            )
        if le > 1:
            if counts[1] == counts[0]:
                title = ':first_place: Egzekwo'
            else:
                title = ':second_place: Drugie miejsce'
            em.add_field(
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
            em.add_field(
                name=title,
                value='{0[2]} \u2015 **{1[2]}**'.format(*f),
                inline=False
            )
    return em
