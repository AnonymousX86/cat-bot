# -*- coding: utf-8 -*-
from asyncio import sleep
from random import choice

from discord import Forbidden, Member
from discord.ext.commands import Cog, command, Context, cooldown, BucketType

from CatBot.embeds.core import ErrorEmbed
from CatBot.embeds.responses import MonologEmbed, IpEmbed


class Responses(Cog, name='Proste odpowiedzi'):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='spierdalaj',
        biref='Każe komuś... Spierdalać',
        usage='[użytkownik]'
    )
    async def spierdalaj(self, ctx: Context, member: Member = None):
        if member:
            await ctx.send(f'Dokładnie, spierdalaj {member.mention}.')
        else:
            await ctx.message.reply('Sam spierdalaj.')

    @command(
        name='ziomek',
        brief='Że kto?'
    )
    async def ziomek(self, ctx: Context):
        await ctx.message.reply('Ty przecież kolegów nie masz.')

    @command(
        name='kurwo',
        brief='Chyba Ty'
    )
    async def kurwo(self, ctx: Context):
        await ctx.message.reply('Ej chuju.')

    @cooldown(1, 7200, BucketType.guild)
    @command(
        name='kurwa',
        brief='Synonimy i wyrazy podobne',
        description='Użycie tej komendy grozi wyciszeniem lub banem.'
    )
    async def kurwa(self, ctx: Context):
        await ctx.message.reply('No dobra...')
        await sleep(3)
        # noinspection SpellCheckingInspection
        for text in sorted(
                'dokurwić, dokurwiać, kurwieć, kurwić się, kurwować, nakurwić'
                ' się, nakurwiać, odkurwić, odkurwiać, okurwiać, okurwić,'
                ' poodkurwiać, popodkurwiać, poprzekurwiać, poprzykurwiać,'
                ' porozkurwiać, poskurwiać, powkurwiać, powykurwiać,'
                ' pozakurwiać, przekurwić, przekurwiać, przykurwić, rozkurwić,'
                ' rozkurwiać, skurwieć, skurwić, skurwiać, ukurwiać, wkurwić,'
                ' wkurwiać, wykurwić, zakurwić, zakurwiać, kurewstwo, kurwiarz,'
                ' kurwiątko, kurwica, kurwidołek, kurwie macierze syn kurwik,'
                ' kurwiszcze, kurwiszon, skurwiel, skurwysyn, podkurw, pokurw,'
                ' rozkurw, wkurw, zakurw, kurewski, kurwi, kurwowaty,'
                ' kurwujący, podkurwiony, przekurwiony, przykurwiony,'
                ' rozkurwiony, skurwiały, wkurwiający, wkurwiony, zakurwiony,'
                ' kurna chata, kurna Olek, kurwa mać, kurwa twoja mać była,'
                ' do kurwy nędzy, o kurwa, dziwka, kurtyzana, nierządnica,'
                ' prostytutka, tirówka, cichodajka, dupodajka, jawnogrzesznica,'
                ' ladacznica, lafirynda, latawica, ruchawica, suka, szmata,'
                ' wszetecznica, wywłoka, zdzira,  łajdak, sprzedawczyk,'
                ' nikczemnik, palant, dupek'.split(', ')
        ):
            await ctx.send(text)
            await sleep(0.5)

    @command(
        name='skryba',
        brief='Monolog skryby'
    )
    async def skryba(self, ctx: Context):
        await ctx.send(embed=MonologEmbed())

    @command(
        name='delet',
        brief='Delet dis now!!1!'
    )
    async def delet(self, ctx: Context, member: Member = None):
        if member:
            await ctx.send(f'{member.mention} usuń to.')
        await ctx.send(
            'https://media.discordapp.net/attachments/662715159961272320/'
            '776709279507808276/trigger-cut.gif'
        )
        try:
            await ctx.message.delete()
        except Forbidden:
            pass

    @command(
        name='2137',
        biref='Śpiewa barkę',
        aliases=['janpawel', 'janpaweł', 'JanPawel', 'JanPaweł']
    )
    async def cmd_2137(self, ctx: Context):
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
            await ctx.send(f'*{line}*')
            await sleep(3)

    @command(
        name='ip',
        brief='IP bota'
    )
    async def ip(self, ctx: Context):
        await ctx.send(embed=IpEmbed())

    @command(
        name='obelga',
        brief='Wymyśla pojazd na kimś',
        description='Losuje osobę z kanału ProtonVPN i dodaje obelgę. Na'
                    ' kanale muszą być przynajmniej 3 osoby.',
        aliases=['pojazd', 'samochód']
    )
    async def obelga(self, ctx: Context):
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
        ]).format(choice(list(map(lambda u: u.mention,
                                  filter(lambda u: not u.bot, ch.members))))))


def setup(bot):
    bot.add_cog(Responses(bot))
