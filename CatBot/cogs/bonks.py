# -*- coding: utf-8 -*-
from discord import Member
from discord.ext.commands import Cog, command, Context

from CatBot.embeds.bonks import BonkEmbed, BonksEmbed
from CatBot.embeds.core import MissingMemberEmbed, ErrorEmbed
from CatBot.utils.database import add_bonk, get_bonks


class Bonks(Cog, name='Bonkowanie'):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='bonk',
        brief='Ktoś dostaje bonka',
        description='Go to horny jail!',
        usage='<użytkownik>'
    )
    async def bonk(self, ctx: Context, member: Member = None):
        if not member:
            return await ctx.send(embed=MissingMemberEmbed())
        elif member.id == ctx.author.id:
            return await ctx.send(embed=ErrorEmbed(
                'Nie możesz sam siebie zbonkować'
            ))
        if not add_bonk(member.id):
            return await ctx.send(embed=ErrorEmbed(
                '**\\*BONK!\\***, ale... Coś poszło nie tak. Anon ratuj!'
            ))
        await ctx.send(embed=BonkEmbed(member))

    @command(
        name='bonki',
        brief='Sprawdź liczbę bonków',
        usage='<użytkownik>'
    )
    async def bonki(self, ctx: Context, member: Member = None):
        if not member:
            return await ctx.send(embed=MissingMemberEmbed())
        await ctx.send(embed=BonksEmbed(get_bonks(member.id), member))


def setup(bot):
    bot.add_cog(Bonks(bot))
