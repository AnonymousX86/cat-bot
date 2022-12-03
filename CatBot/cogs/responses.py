# -*- coding: utf-8 -*-
from asyncio import sleep
from random import choice

from discord import slash_command, ApplicationContext
from discord.ext.commands import Cog

from CatBot.embeds.core import ErrorEmbed
from CatBot.embeds.responses import MonologEmbed, IpEmbed, PatEmbed, HugEmbed, \
    InsultEmbed
from CatBot.settings import DEFAULT_MEMBER_OPTION
from CatBot.utils.members import random_member


class Responses(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name='skryba',
        description='Monolog skryby.'
    )
    async def skryba(self, ctx: ApplicationContext):
        await ctx.send_response(embed=MonologEmbed())

    @slash_command(
        name='delet',
        description='Nakaż komuś zrobić "delet"'
    )
    async def delet(self, ctx: ApplicationContext):
        await ctx.send_response(
            'https://media.discordapp.net/attachments/662715159961272320/'
            '776709279507808276/trigger-cut.gif'
        )

    @slash_command(
        name='2137',
        description='Toż to papieżowa liczba.'
    )
    async def cmd_2137(self, ctx: ApplicationContext):
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
                await ctx.send_response(f'*{line}*')
                first = False
            await sleep(3)

    @slash_command(
        name='ip',
        description='IP bota.'
    )
    async def ip(self, ctx: ApplicationContext):
        await ctx.send_response(embed=IpEmbed())

    @slash_command(
        name='obelga',
        description='Losuje osobę z kanału głosowego i dodaje obelgę. Na'
                    ' kanale muszą być przynajmniej 3 osoby.'
    )
    async def insult(self, ctx: ApplicationContext):
        occupied_channels = list(
            filter(lambda ch: len(ch.members), ctx.guild.voice_channels))
        if not occupied_channels:
            await ctx.send_response(embed=ErrorEmbed(
                'Żaden kanał nie jest zajęty.'
            ))
        elif len(
                (first_channel := sorted(
                    occupied_channels,
                    key=lambda ch: len(ch.members)
                )[0]).members
        ) < 3:
            await ctx.send_response(embed=ErrorEmbed(
                f'Na kanale **{first_channel.name}** jest zbyt mało użytkowników'
            ))
        else:
            await ctx.send_response(embed=InsultEmbed(choice([
                '{}, a Twój stary to Twoja stara.',
                '{} Twoje auto nie ma okien.',
                '{} udław się kokosem.',
                '{} wsadź se szyszkę w dupę.',
                '{} wyjmij mikrofon z dupy.',
                '{} jak Ci walnę w zęby, to będziesz je mył wsadzając sobie'
                ' szczoteczkę do dupy.',
                '{} Twój pies sra mordą.'
            ]).format(choice(list(map(
                lambda m: m.mention,
                filter(lambda m: m.bot is False, first_channel.members)
            ))))))

    @slash_command(
        name='pac',
        description='Pacnij kogoś.'
    )
    async def pat(
            self,
            ctx: ApplicationContext,
            member: DEFAULT_MEMBER_OPTION
    ):
        if not member:
            member = random_member(ctx.guild.members)
        await ctx.send_response(embed=PatEmbed(member, ctx.user))

    @slash_command(
        name='przytul',
        description='Przytul kogoś.'
    )
    async def hug(
            self,
            ctx: ApplicationContext,
            member: DEFAULT_MEMBER_OPTION
    ):
        if not member:
            member = random_member(ctx.guild.members)
        await ctx.send_response(embed=HugEmbed(member, ctx.user))


def setup(bot):
    bot.add_cog(Responses(bot))
