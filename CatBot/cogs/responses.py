# -*- coding: utf-8 -*-
from asyncio import sleep
from random import choice

from discord import Member
from discord.ext.commands import Cog
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from CatBot.embeds.core import ErrorEmbed
from CatBot.embeds.responses import MonologEmbed, IpEmbed, PatEmbed, HugEmbed
from CatBot.settings import bot_guilds, dev_guilds


class Responses(Cog, name='Proste odpowiedzi'):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='skryba',
        description='Monolog skryby.',
        guild_ids=bot_guilds()
    )
    async def skryba(self, ctx: SlashContext):
        await ctx.send(embed=MonologEmbed())

    @cog_ext.cog_slash(
        name='delet',
        description='Delet dis now!!1!',
        guild_ids=bot_guilds()
    )
    async def delet(self, ctx: SlashContext):
        await ctx.send(
            'https://media.discordapp.net/attachments/662715159961272320/'
            '776709279507808276/trigger-cut.gif'
        )

    @cog_ext.cog_slash(
        name='2137',
        description='Toż to papieżowa liczba.',
        guild_ids=bot_guilds()
    )
    async def cmd_2137(self, ctx: SlashContext):
        first = True
        for line in [
            'Pan kiedyś stanął nad brzegiem,',
            'Szukał ludzi gotowych pójść za Nim;',
            'By łowić serca',
            'Słów Bożych prawdą.',
            '\\*inhales\\*',
            'O Panie, to Ty na mnie spojrzałeś,',
            'Twoje usta dziś wyrzekły me imię.',
            'Swoją barkę pozostawiam na brzegu,',
            'Razem z Tobą nowy zacznę dziś łów.'
        ]:
            if not first:
                await ctx.channel.send(f'*{line}*')
            else:
                await ctx.send(f'*{line}*')
                first = False
            await sleep(3)

    @cog_ext.cog_slash(
        name='ip',
        description='IP bota.',
        guild_ids=dev_guilds()
    )
    async def ip(self, ctx: SlashContext):
        await ctx.send(embed=IpEmbed())

    @cog_ext.cog_slash(
        name='obelga',
        description='Losuje osobę z kanału ProtonVPN i dodaje obelgę. Na'
                    ' kanale muszą być przynajmniej 3 osoby.',
        guild_ids=bot_guilds()
    )
    async def obelga(self, ctx: SlashContext):
        ch = ctx.guild.get_channel(385122529343176709)
        if len(ch.members) < 3:
            return await ctx.send(embed=ErrorEmbed(
                f'Za mało użytkowników na `{ch}`.'
            ))
        await ctx.send(choice([
            '{}, a Twój stary to Twoja stara.',
            '{} Twoje auto nie ma okien.',
            '{} udław się kokosem.',
            '{} wsadź se szyszkę w dupę.',
            '{} wyjmij mikrofon z dupy.',
            '{} jak Ci walnę w zęby, to będziesz je mył wsadzając sobie'
            ' szczoteczkę do dupy.',
            '{} Twój pies sra mordą.'
        ]).format(choice(list(map(
            lambda u: u.mention,
            filter(lambda u: not u.bot, ch.members)
        )))))

    @cog_ext.cog_slash(
        name='pac',
        description='Pacnij kogoś.',
        guild_ids=bot_guilds(),
        options=[
            create_option(
                name='uzytkownik',
                description='Wybierz kogoś z serwera',
                option_type=6,
                required=True
            )
        ]
    )
    async def pac(self, ctx: SlashContext, uzytkownik: Member):
        await ctx.send(embed=PatEmbed(uzytkownik, ctx.author))

    @cog_ext.cog_slash(
        name='tuli',
        description='Przytul kogoś.',
        guild_ids=bot_guilds(),
        options=[
            create_option(
                name='uzytkownik',
                description='Wybierz kogoś z serwera',
                option_type=6,
                required=True
            )
        ]
    )
    async def tuli(self, ctx: SlashContext, uzytkownik: Member):
        await ctx.send(embed=HugEmbed(uzytkownik, ctx.author))


def setup(bot):
    bot.add_cog(Responses(bot))
