# -*- coding: utf-8 -*-
from discord import Member
from discord.ext.commands import Cog, command, Context

from CatBot.embeds.basic import missing_user_em, custom_error_em
from CatBot.embeds.bonks import bonks_em, bonk_em
from CatBot.utils.database import add_bonk, get_bonks


class Bonks(Cog):
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
            return await ctx.message.reply(embed=missing_user_em())
        if not add_bonk(member.id):
            return await ctx.message.reply(embed=custom_error_em(
                '**\\*BONK!\\***, ale... Coś poszło nie tak. Anon ratuj!'
            ))
        await ctx.message.reply(embed=bonk_em(member))

    @command(
        name='bonki',
        brief='Sprawdź liczbę bonków',
        usage='<użytkownik>'
    )
    async def bonki(self, ctx: Context, member: Member = None):
        if not member:
            return await ctx.message.reply(embed=missing_user_em())
        await ctx.message.reply(embed=bonks_em(get_bonks(member.id), member))


def setup(bot):
    bot.add_cog(Bonks(bot))
