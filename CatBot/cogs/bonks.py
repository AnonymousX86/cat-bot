# -*- coding: utf-8 -*-
from discord import Member
from discord.ext.commands import Cog
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from CatBot.embeds.bonks import BonkEmbed, BonksEmbed
from CatBot.embeds.core import ErrorEmbed
from CatBot.settings import bot_guilds
from CatBot.utils.database import add_bonk, get_bonks


class Bonks(Cog, name='Bonkowanie'):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='bonk',
        description='Daje komuś bonka. Go to horny jail!',
        guild_ids=bot_guilds(),
        options=[
            create_option(
                name='uzytkownik',
                description='Wybierz kogoś z serwera.',
                option_type=6,
                required=True
            )
        ]
    )
    async def bonk(self, ctx: SlashContext, uzytkownik: Member):
        if uzytkownik.id == ctx.author.id:
            return await ctx.send(embed=ErrorEmbed(
                'Nie możesz sam siebie zbonkować'
            ))
        if not add_bonk(uzytkownik.id):
            return await ctx.send(embed=ErrorEmbed(
                '**\\*BONK!\\***, ale... Coś poszło nie tak. Anon ratuj!'
            ))
        await ctx.send(embed=BonkEmbed(uzytkownik))

    @cog_ext.cog_slash(
        name='bonki',
        description='Sprawdź liczbę bonków',
        guild_ids=bot_guilds(),
        options=[
            create_option(
                name='uzytkownik',
                description='Wybierz kogoś z serwera. Jeżeli nie - bot wybierze'
                            ' Ciebie.',
                option_type=6,
                required=False
            )
        ]
    )
    async def bonki(self, ctx: SlashContext, uzytkownik: Member = None):
        if not uzytkownik:
            uzytkownik = ctx.author
        await ctx.send(embed=BonksEmbed(get_bonks(uzytkownik.id), uzytkownik))


def setup(bot):
    bot.add_cog(Bonks(bot))
