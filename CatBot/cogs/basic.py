# -*- coding: utf-8 -*-
from discord import Message
from discord.ext.commands import Cog, command, Context

from CatBot.embeds.basic import *


class Basic(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='info'
    )
    async def info(self, ctx: Context):
        await ctx.send(embed=info_em())

    @Cog.listener('on_message')
    async def plus_adder(self, message: Message = None):
        if message.channel.id in [773548753428152390]:
            await message.add_reaction('👍')
            await message.add_reaction('👎')

    @command(
        name='minecraft',
        aliases=['mc']
    )
    async def minecraft(self, ctx: Context):
        msg = await ctx.send(embed=please_wait_em())
        await ctx.send(embed=mc_embed())
        await msg.delete()

    @command(
        name='archiwa',
        aliases=['archives', 'arch']
    )
    async def archiwa(self, ctx: Context):
        await ctx.send(embed=archives_embed())


def setup(bot):
    bot.add_cog(Basic(bot))
