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

    @command(
        name='ip'
    )
    async def ip(self, ctx: Context):
        await ctx.send(embed=ip_em())

    @command(
        name='spierdalaj'
    )
    async def spierdalaj(self, ctx: Context, user: Optional[Member]):
        if user:
            await ctx.send(f'Dokładnie, spierdalaj {user.mention}.')
        else:
            await ctx.send('Sam spierdalaj.')

    @command(
        name='ziomek'
    )
    async def ziomek(self, ctx: Context):
        await ctx.send('Ty przecież kolegów nie masz.')

    @command(
        name='kurwo'
    )
    async def kurwo(self, ctx: Context):
        await ctx.send('Ej chuju.')

    @command(
        name='kurwa',
        description='Wysyła wszystkie synonimy i wyrazy podobne'
    )
    async def kurwa(self, ctx: Context):
        await ctx.send('No dobra...')
        await sleep(3)
        # noinspection SpellCheckingInspection
        for text in sorted([
            *'dokurwić, dokurwiać, kurwieć, kurwić się, kurwować, nakurwić się, nakurwiać, odkurwić, odkurwiać,'
             ' okurwiać, okurwić, podkurwić, podkurwiać, pokurwić, pokurwiać, pokurwieć, podokurwiać, ponakurwiać,'
             ' poodkurwiać, popodkurwiać, poprzekurwiać, poprzykurwiać,porozkurwiać, poskurwiać, powkurwiać,'
             ' powykurwiać, pozakurwiać, przekurwić, przekurwiać, przykurwić, rozkurwić, rozkurwiać, skurwieć,'
             ' skurwić, skurwiać, ukurwiać, wkurwić, wkurwiać, wykurwić, zakurwić, zakurwiać,'
             ' kurewstwo, kurwiarz, kurwiątko, kurwica, kurwidołek, kurwie macierze syn kurwik, kurwiszcze, kurwiszon,'
             ' skurwiel, skurwysyn, podkurw, pokurw, rozkurw, wkurw, zakurw, kurewski, kurwi, kurwowaty, kurwujący,'
             ' podkurwiony, przekurwiony, przykurwiony, rozkurwiony, skurwiały, wkurwiający, wkurwiony,'
             ' zakurwiony, kurewsko, wykurwiście, na pełnej kurwie, od kurwy, w kurwę, kurde, kurna, kuźwa,'
             ' kurna chata, kurna Olek, kurwa mać, kurwa twoja mać była, do kurwy nędzy, o kurwa, dziwka, kurtyzana,'
             ' nierządnica, prostytutka, tirówka, cichodajka, dupodajka, jawnogrzesznica, ladacznica, lafirynda,'
             ' latawica, ruchawica, suka, szmata, wszetecznica, wywłoka, zdzira,  łajdak, sprzedawczyk, nikczemnik,'
             ' palant, dupek'.split(', ')
        ]):
            await ctx.send(text)
            await sleep(0.5)

    @command(
        name='skryba'
    )
    async def skryba(self, ctx: Context):
        await ctx.send(embed=skryba_em())

    @command(
        name='delet'
    )
    async def delet(self, ctx: Context, member: Optional[Member]):
        if member:
            await ctx.send(f'{member.mention} usuń to.')
        await ctx.send(
            'https://media.discordapp.net/attachments/662715159961272320/776709279507808276/trigger-cut.gif'
        )
        try:
            await ctx.message.delete()
        except Forbidden:
            pass

    @command(
        name='2137',
        aliases=['janpawel', 'janpaweł', 'JanPawel', 'JanPaweł']
    )
    async def cmd_2137(self, ctx: Context):
        text = [
            'Pan kiedyś stanął nad brzegiem,',
            'Szukał ludzi gotowych pójść za Nim;',
            'By łowić serca',
            'Słów Bożych prawdą.',
            'Ref.: O Panie, to Ty na mnie spojrzałeś,',
            'Twoje usta dziś wyrzekły me imię.',
            'Swoją barkę pozostawiam na brzegu,',
            'Razem z Tobą nowy zacznę dziś łów.'
        ]
        for line in text:
            await ctx.send(f'*{line}*')
            await sleep(3)


def setup(bot):
    bot.add_cog(Basic(bot))
