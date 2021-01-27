# -*- coding: utf-8 -*-
from asyncio import sleep
from typing import Optional

from discord import Message, HTTPException, Forbidden, NotFound
from discord.ext.commands import Cog, command, Context
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import SearchVideos

from CatBot.embeds.basic import *


class Basic(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='info',
        breif='Podstawowe informacje na temat bota'
    )
    async def info(self, ctx: Context):
        await ctx.send(embed=info_em())

    @Cog.listener('on_message')
    async def plus_adder(self, message: Message = None):
        if message.channel.id in [773548753428152390]:
            await message.add_reaction('👍')
            await message.add_reaction('👎')

    @Cog.listener('on_message')
    async def spotify_to_youtube(self, message: Message):
        if message.channel.id not in [782312754220105738]:
            if message.content.startswith('https://open.spotify.com/track/'):
                sp = Spotify(
                    auth_manager=SpotifyClientCredentials(
                        client_id='11fb31af174d46218d05049e75d0a8a8',
                        client_secret=Settings().spotify_secret
                    )
                )
                result = sp.track(message.content.split('/')[-1])
                yt = SearchVideos(
                    '{} {}'.format(result['name'], ' '.join(map(lambda x: x['name'], result['artists']))),
                    mode='dict',
                    max_results=1
                ).result()['search_result'][0]['link']
                await message.channel.send(embed=spotify_em(result, message.author))
                await message.channel.send(f'**YouTube**\n{yt}')
                try:
                    await message.delete()
                except Forbidden or HTTPException or NotFound:
                    pass

    @command(
        name='archiwa',
        brief='Dostępne pliki powiązane z naszym Discordem',
        aliases=['archives', 'arch']
    )
    async def archiwa(self, ctx: Context):
        await ctx.send(embed=archives_embed())

    @command(
        name='ip',
        brief='IP bota'
    )
    async def ip(self, ctx: Context):
        await ctx.send(embed=ip_em())

    @command(
        name='autorole',
        biref='Aktualizacja ról',
        description='Dostępne tylko dla Anona.',
        hidden=True
    )
    async def autorole(self, ctx: Context):
        if ctx.author.id != 309270832683679745:
            await ctx.send(embed=missing_perms_em())
        else:
            msg = await ctx.send(embed=please_wait_em())
            added = 0
            for member in ctx.guild.members:
                if not member.bot:
                    for role in map(lambda x: ctx.guild.get_role(x), [718576689302470795, 720650395977777294]):
                        try:
                            await member.add_roles(role, reason='Automatyzacja ról.')
                        except Forbidden:
                            await ctx.send(
                                f'Nie mogę dać roli `{role}` użytkownikowi {member.display_name}'
                            )
                        except HTTPException:
                            pass
                        else:
                            added += 1
            await ctx.send(embed=done_em(f'Zaktualizowana ilość ról: {added}.'))
            await msg.delete()

    @command(
        name='spierdalaj',
        biref='Każe komuś... Spierdalać'
    )
    async def spierdalaj(self, ctx: Context, user: Optional[Member]):
        if user:
            await ctx.send(f'Dokładnie, spierdalaj {user.mention}.')
        else:
            await ctx.send('Sam spierdalaj.')

    @command(
        name='ziomek',
        brief='Że kto?'
    )
    async def ziomek(self, ctx: Context):
        await ctx.send('Ty przecież kolegów nie masz.')

    @command(
        name='kurwo',
        brief='Chyba Ty'
    )
    async def kurwo(self, ctx: Context):
        await ctx.send('Ej chuju.')

    @command(
        name='kurwa',
        brief='Synonimy i wyrazy podobne'
    )
    async def kurwa(self, ctx: Context):
        await ctx.send('No dobra...')
        await sleep(3)
        # noinspection SpellCheckingInspection
        for text in sorted([
            *'dokurwić, dokurwiać, kurwieć, kurwić się, kurwować, nakurwić się, nakurwiać, odkurwić, odkurwiać,'
             ' okurwiać, okurwić, podkurwić, podkurwiać, pokurwić, pokurwiać, pokurwieć, podokurwiać, ponakurwiać,'
             ' poodkurwiać, popodkurwiać, poprzekurwiać, poprzykurwiać, porozkurwiać, poskurwiać, powkurwiać,'
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
        name='skryba',
        brief='Monolog skryby'
    )
    async def skryba(self, ctx: Context):
        await ctx.send(embed=skryba_em())

    @command(
        name='delet',
        brief='Delet dis now!!1!'
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
        biref='Śpiewa barkę',
        aliases=['janpawel', 'janpaweł', 'JanPawel', 'JanPaweł']
    )
    async def cmd_2137(self, ctx: Context):
        text = [
            'Pan kiedyś stanął nad brzegiem,',
            'Szukał ludzi gotowych pójść za Nim;',
            'By łowić serca',
            'Słów Bożych prawdą.',
            '\\*inhales\\*',
            'O Panie, to Ty na mnie spojrzałeś,',
            'Twoje usta dziś wyrzekły me imię.',
            'Swoją barkę pozostawiam na brzegu,',
            'Razem z Tobą nowy zacznę dziś łów.'
        ]
        for line in text:
            await ctx.send(f'*{line}*')
            await sleep(3)

    # noinspection SpellCheckingInspection
    @command(
        name='order',
        brief='Odznacza kogoś orderem Sashy Grey'
    )
    async def order(self, ctx: Context, user: Member):
        if not user:
            await ctx.send(embed=missing_user_em())
        elif 641331138622783508 not in map(lambda r: r.id, ctx.author.roles):
            await ctx.send(embed=missing_perms_em())
        else:
            try:
                await user.add_roles(ctx.guild.get_role(799377826859843634), reason='Przeruchanie przeruchanego mema.')
            except HTTPException:
                pass
            await ctx.send(embed=done_em(
                f'{user.mention} otrzymał(a) **order Sashy Grey** za **przeruchanie przeruchanego mema**.'
            ))


def setup(bot):
    bot.add_cog(Basic(bot))
