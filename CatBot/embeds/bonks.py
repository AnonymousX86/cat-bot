# -*- coding: utf-8 -*-
from discord import Embed, Member

from CatBot.embeds.custom_classes import BaseEmbed, SuccessEmbed


def bonk_em(member: Member) -> Embed:
    return SuccessEmbed(
        title=':moyai: \\*BONK!\\*',
        description=f'{member.mention} go to horny jail.'
    )


def bonks_em(count: int, member: Member) -> Embed:
    return BaseEmbed(
        title=':moyai: Horny\'o\'meter',
        description=f'{member.mention} ' + (
            'jest czysty(a).' if count == 0 else f'ma **{count}** bonk{"a" if count == 1 else "ów"}.'
        )
    )
