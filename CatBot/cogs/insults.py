# -*- coding: utf-8
from datetime import datetime
from random import Random

from discord.ext.commands import Cog, Context
from discord_slash import cog_ext

from CatBot.embeds.insults import InsultEmbed
from CatBot.settings import bot_guilds


class CustomRandom(Random):
    def __init__(self, seed=datetime.now().strftime('%Y%m%d').encode('utf-8')):
        super().__init__(seed)

    def choice(self, seq):
        return super().choice(seq)


class Insults(Cog, name='Insults'):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='kogo_obrazic',
        description='Losuje z serwera kogo dzisiaj obrażamy.',
        guild_ids=bot_guilds()
    )
    async def kogo_obrazic(self, ctx: Context):
        await ctx.send(embed=InsultEmbed(CustomRandom().choice(
                list(filter(lambda m: not m.bot, ctx.guild.members))
        )))


def setup(bot):
    bot.add_cog(Insults(bot))
