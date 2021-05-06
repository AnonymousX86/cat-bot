# -*- coding: utf-8 -*-
from discord.ext.commands import Cog, command, Context
from wavelink import Client

from CatBot.embeds.core import ErrorEmbed, DoneEmbed


class Music(Cog, name='Muzyka'):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        # noinspection SpellCheckingInspection
        await self.bot.wavelink.initiate_node(
            host='127.0.0.1',
            port='2333',
            rest_uri='http://127.0.0.1:2333',
            password='youshallnotpass',
            identifier='TEST',
            region='us_central'
        )

    @command(
        name='connect'
    )
    async def connect_(self, ctx: Context):
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            return await ctx.message.reply(
                embed=ErrorEmbed('Dołącz się gdzieś'))

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.connect(channel.id)

    @command(
        name='play'
    )
    async def play(self, ctx: Context, *, query: str = None):
        if not query:
            return await ctx.message.reply(
                embed=ErrorEmbed('Co mam włączyć?'))

        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')
        if not tracks:
            return await ctx.message.reply(embed=ErrorEmbed('Nic nie ma'))

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        await ctx.message.reply(
            embed=DoneEmbed(f'Dodano {str(tracks[0])} do kolejki'))
        await player.play(tracks[0])


def setup(bot):
    bot.add_cog(Music(bot))
