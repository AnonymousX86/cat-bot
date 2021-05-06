# -*- coding: utf-8 -*-
from discord import Member

from CatBot.embeds.core import DoneEmbed


class BonkEmbed(DoneEmbed):
    def __init__(self, member: Member, **kwargs):
        super().__init__(**kwargs)
        self.title = ':moyai: \\*BONK!\\*'
        self.description = f'{member.mention} go to horny jail.'


class BonksEmbed(DoneEmbed):
    def __init__(self, count: int, member: Member, **kwargs):
        super().__init__(**kwargs)
        self.title = ':moyai: Horny\'o\'meter'
        self.description = f'{member.mention} ' + (
            'jest czysty(a).' if count == 0 else
            f'ma **{count}** bonk{"a" if count == 1 else "ów"}.'
        )
