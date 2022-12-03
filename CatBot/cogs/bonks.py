# -*- coding: utf-8 -*-
from discord import Member, ApplicationContext, user_command, slash_command
from discord.ext.commands import Cog

from CatBot.embeds.bonks import BonkEmbed, BonksEmbed
from CatBot.embeds.core import ErrorEmbed, PleaseWaitEmbed
from CatBot.settings import DEFAULT_MEMBER_OPTION
from CatBot.utils.database import add_bonk, get_bonks


class Bonks(Cog, name='Bonkowanie'):
    def __init__(self, bot):
        self.bot = bot

    @user_command(
        name='Zbonkuj'
    )
    async def bonks_add(self, ctx: ApplicationContext, member: Member):
        if member == ctx.author:
            return await ctx.send_response(embed=ErrorEmbed(
                'Nie możesz sam siebie zbonkować'
            ))
        if not add_bonk(member.id):
            return await ctx.send_response(embed=ErrorEmbed(
                '**\\*BONK!\\***, ale... Coś poszło nie tak. Anon ratuj!'
            ))
        await ctx.send_response(embed=PleaseWaitEmbed())
        await ctx.edit(embed=BonkEmbed(member))

    @slash_command(
        name='bonki',
        description='Sprawdź ile kto ma bonków'
    )
    async def bonks_check(
            self,
            ctx: ApplicationContext,
            member: DEFAULT_MEMBER_OPTION
    ):
        if not member:
            member = ctx.message.author
        await ctx.send_response(embed=PleaseWaitEmbed())
        await ctx.edit(embed=BonksEmbed(
            get_bonks(member.id), member)
        )


def setup(bot):
    bot.add_cog(Bonks(bot))
