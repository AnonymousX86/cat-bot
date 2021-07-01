# -*- coding: utf-8 -*-
from discord import Member

from CatBot.embeds.core import DoneEmbed


class CountersEmbed(DoneEmbed):
    def __init__(self, member: Member, reason: str, count: int, **kwargs):
        super().__init__(**kwargs)
        self.title = ':abacus: Countery'
        self.description = f'{member.mention} {reason}' \
                           f' {count} raz{"" if count == 1 else "y"}.'


class CounterAddedEmbed(DoneEmbed):
    def __init__(self, member: Member, reason: str, count: int, **kwargs):
        super().__init__(**kwargs)
        self.title = '<:green_plus:683603513728696333> Counter!'
        self.description = f'{member.mention} dostał(a) countera,' \
                           f' więc {reason} {count}' \
                           f' raz{"" if count == 1 else "y"}.'


class InterruptsEmbed(DoneEmbed):
    def __init__(self, member: Member, count: int, **kwargs):
        super().__init__(**kwargs)
        self.title = ':abacus: Przerwane zdania'
        self.description = f'{member.mention} przerwał(a) zdanie' \
                           f' {count} raz{"y" if count != 1 else ""}.'


class InterruptAddedEmbed(DoneEmbed):
    def __init__(self, member: Member, count: int, **kwargs):
        super().__init__(**kwargs)
        self.title = ':slight_smile: Dzięki'
        self.description = f'{member.mention} znowu przerwał(a) zdanie,' \
                           f' czyli zrobił(a) to łącznie {count}' \
                           f' raz{"y" if count != 1 else ""}.'
