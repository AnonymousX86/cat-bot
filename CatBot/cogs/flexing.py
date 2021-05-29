# -*- coding: utf-8 -*-
from discord import User, Member
from discord.ext.commands import Cog
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from CatBot.embeds.core import ErrorEmbed
from CatBot.embeds.flexing import FlexesEmbed, FlextopEmbed, FlexAddedEmbed
from CatBot.settings import bot_guilds
from CatBot.utils.database import add_flex, get_flexes, get_top_flexes


class Flexing(Cog, name='Flexowanie'):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='flex',
        description='Liczenie flexów w celu jakże użytecznych statystyk, kto'
                    ' jest największym flexiarzem.',
        guild_ids=bot_guilds(),
        options=[
            create_option(
                name='uzytkownik',
                description='Wybierz kogoś z serwera.',
                option_type=6,
                required=True
            ),
            create_option(
                name='opis',
                description='Opisz flexa, najlepiej w 3. formie osobowej.',
                option_type=3,
                required=True
            )
        ]
    )
    async def flex(self, ctx: SlashContext, uzytkownik: Member, opis: str):
        if ctx.author.id == uzytkownik.id:
            return await ctx.send(embed=ErrorEmbed(
                'Ziomek, dostajesz flexa za flexa dając flexa i flexując'
                ' siebie... Serio?!'
            ))
        elif not add_flex(uzytkownik.id, opis):
            return await ctx.message.reply(
                embed=ErrorEmbed('Nie mogę dodać flexa tej osobie.'))
        else:
            return await ctx.send(embed=FlexAddedEmbed(uzytkownik, opis))

    @cog_ext.cog_slash(
        name='flexy',
        description='Pokazuje czyjeś flexy.',
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
    async def flexy(self, ctx: SlashContext, uzytkownik: User = None):
        if not uzytkownik:
            uzytkownik = ctx.author
        flexes = get_flexes(uzytkownik.id)
        await ctx.send(embed=FlexesEmbed(uzytkownik, flexes))

    @cog_ext.cog_slash(
        name='flextop',
        description='Lista osób, które najwięcej się flexują.',
        guild_ids=bot_guilds(),
        options=[
            create_option(
                name='dni',
                description='Uwzględnij statystyki tylko z X ostanich dni.',
                option_type=4,
                required=False
            )
        ]
    )
    async def flextop(self, ctx: SlashContext, dni: int = 30):
        min_ = 2
        if dni < min_:
            return await ctx.send(embed=ErrorEmbed(
                f'Podaj co najmniej {min_}!'
            ))
        flexes = get_top_flexes(dni)
        users = [i for i in
                 map(lambda x: ctx.guild.get_member(int(x[0])).mention, flexes)]
        counts = [i for i in map(lambda x: x[1], flexes)]
        await ctx.send(embed=FlextopEmbed(users, counts, dni))


def setup(bot):
    bot.add_cog(Flexing(bot))
