# -*- coding: utf-8 -*-
from discord import ApplicationContext, user_command, slash_command
from discord.ext.commands import Cog

from CatBot.embeds.core import ErrorEmbed, PleaseWaitEmbed
from CatBot.embeds.counters import CounterAddedEmbed, CountersEmbed, \
    InterruptsEmbed, InterruptAddedEmbed
from CatBot.settings import COUNTERS, DEFAULT_MEMBER_OPTION
from CatBot.utils.database import get_counters, add_counter, add_interrupt, \
    get_interrupts


class Counters(Cog):
    def __init__(self, bot):
        self.bot = bot

    @user_command(
        name='Dodaj Counter'
    )
    async def counters_add(
            self,
            ctx: ApplicationContext,
            member: DEFAULT_MEMBER_OPTION
    ):
        await ctx.send_response(embed=PleaseWaitEmbed())
        if not (counter := COUNTERS.get(str(member.id))):
            await ctx.edit(embed=ErrorEmbed(
                f'{member.mention} nie ma counterów.'
            ))
        elif not add_counter(member.id):
            await ctx.edit(embed=ErrorEmbed(
                f'Nie mogę dodać countera {member.mention}'
            ))
        else:
            await ctx.edit(embed=CounterAddedEmbed(
                member,
                counter,
                get_counters(member.id)
            ))


    @slash_command(
        name='countery',
        description='Sprawdź ile ktoś ma "counterów".'
    )
    async def counters_check(
            self,
            ctx: ApplicationContext,
            member: DEFAULT_MEMBER_OPTION
    ):
        if not member:
            member = ctx.author
        await ctx.send_response(embed=PleaseWaitEmbed())
        if not (counter := COUNTERS.get(str(member.id))):
            await ctx.edit(embed=ErrorEmbed(
                f'{member.mention} nie ma counterów.'
            ))
            return
        await ctx.edit(embed=CountersEmbed(
            member,
            counter,
            get_counters(member.id)
        ))


    @user_command(
        name='Wtrącił Się W Zdanie'
    )
    async def interrupts_add(
            self,
            ctx: ApplicationContext,
            member: DEFAULT_MEMBER_OPTION
    ):
        await ctx.send_response(embed=PleaseWaitEmbed())
        if not add_interrupt(member.id):
            await ctx.edit(embed=ErrorEmbed(
                'Wystąpił błąd w zapytaniu do bazy danych.'
            ))
        else:
            await ctx.edit(embed=InterruptAddedEmbed(
                member,
                get_interrupts(member.id)
            ))


    @slash_command(
        name='w_zdanie',
        description='Sprawdź ile razy ktoś wtrącił się w zdanie.'
    )
    async def w_zdanie(
            self,
            ctx: ApplicationContext,
            member: DEFAULT_MEMBER_OPTION
    ):
        if not member:
            member = ctx.user
        await ctx.send_response(embed=PleaseWaitEmbed())
        await ctx.edit(embed=InterruptsEmbed(
            member,
            get_interrupts(member.id)
        ))


def setup(bot):
    bot.add_cog(Counters(bot))
