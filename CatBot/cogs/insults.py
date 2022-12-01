# -*- coding: utf-8
from discord import slash_command, ApplicationContext
from discord.ext.commands import Cog

from CatBot.embeds.insults import BulliedEmbed
from CatBot.utils.members import random_member


class Insults(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name='kogo_obrazic',
        description='Losuje z serwera kogo dzisiaj obrażamy.'
    )
    async def choose_bullied(self, ctx: ApplicationContext):
        await ctx.send_response(embed=BulliedEmbed(random_member(
            ctx.guild.members,
            random_per_day=True
        )))


def setup(bot):
    bot.add_cog(Insults(bot))
