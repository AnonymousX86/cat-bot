# -*- coding: utf-8 -*-
from discord import Message
from discord.ext.commands import Cog, command

from CatBot.templates.basic import *


class Basic(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='info'
    )
    async def info(self, ctx):
        await ctx.send(embed=info_em())

    @Cog.listener('on_message')
    async def plus_adder(self, message: Message = None):
        if message.channel.id in [773548753428152390]:
            await message.add_reaction('👍')
            await message.add_reaction('👎')


def setup(bot):
    bot.add_cog(Basic(bot))
