# -*- coding: utf-8 -*-
from discord import Member

from CatBot.embeds.core import GreenEmbed


class BulliedEmbed(GreenEmbed):
    def __init__(self, member: Member, **kwargs):
        super().__init__(**kwargs)
        self.title = ':twisted_rightwards_arrows: Wylosowałem...'
        self.description = f'Dzisiaj obrażamy {member.mention}'
        self.set_thumbnail(url=member.display_avatar.url)
