# -*- coding: utf-8 -*-
from discord import Message, HTTPException, Forbidden, NotFound, Guild, \
    TextChannel, Member
from discord.ext.commands import Cog
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import SearchVideos

from CatBot.embeds.basic import InfoEmbed, SpotifyEmbed
from CatBot.embeds.core import ErrorEmbed, MissingPermsEmbed, PleaseWaitEmbed, \
    DoneEmbed
from CatBot.settings import spotify_secret, bot_guilds


async def add_basic_roles(guild: Guild, member: Member,
                          channel: TextChannel = None) -> bool:
    success = False
    if not member.bot:
        for role in map(lambda x: guild.get_role(x), [
            628315428384538644,  # Człowieki
            718576689302470795,  # --Gry--
            720650395977777294   # --Inne--
        ]):
            try:
                await member.add_roles(role, reason='Automatyzacja ról.')
            except Forbidden:
                if channel:
                    await channel.send(
                        f'Nie mogę dać roli `{role}` użytkownikowi'
                        f' {member.display_name}')
            except HTTPException:
                pass
            else:
                success = True
    else:
        bot_role = guild.get_role(628315593631727617)
        try:
            await member.add_roles(bot_role, reason='Automatyzacja ról.')
        except Forbidden:
            if channel:
                await channel.send(
                    f'Nie mogę dać roli botowi {member.display_name}')
        except HTTPException:
            pass
        else:
            success = True
    return success


class Basic(Cog, name='Podstawowe'):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='info',
        description='Pokazuje podstawowe informacje na temat bota.'
                    ' (Na co to komu?)',
        guild_ids=bot_guilds()
    )
    async def info(self, ctx: SlashContext):
        await ctx.send(embed=InfoEmbed())

    @Cog.listener('on_member_join')
    async def autorole_updater(self, member: Member):
        await add_basic_roles(member.guild, member)

    @Cog.listener('on_message')
    async def plus_adder(self, message: Message):
        if message.channel.id in [400984666972094465]:
            for emoji in ['👍', '👎']:
                await message.add_reaction(emoji)

    @Cog.listener('on_message')
    async def spotify_to_youtube(self, message: Message):
        if message.channel.id not in [782312754220105738]:
            if message.content.startswith('https://open.spotify.com/track/'):
                sp = Spotify(
                    auth_manager=SpotifyClientCredentials(
                        client_id='11fb31af174d46218d05049e75d0a8a8',
                        client_secret=spotify_secret()
                    )
                )
                if not sp:
                    await message.channel.send(embed=ErrorEmbed(
                        'Nie mogę się połączyć ze Spotify!'
                    ))
                    await self.bot.log.warning('Can\'t connect to Spotify!')
                    return

                result = sp.track(
                    message.content.split('?')[0].split('&')[0].split('/')[-1])
                if not result:
                    await message.channel.send(
                        embed=ErrorEmbed(description='Błędny link Spotify!'))
                    await self.bot.log.info('Spotify link is wrong!')
                    return

                query = '{} {}'.format(result['name'], ' '.join(
                    map(lambda x: x['name'], result['artists'])))
                # noinspection PyTypeChecker
                yt = SearchVideos(
                    query,
                    mode='dict',
                    max_results=1
                ).result()['search_result'][0]['link']
                if not yt:
                    await message.channel.send(embed=ErrorEmbed(
                        'Wyszukiwanie na YouTube - zawiodło.'
                    ))
                    await self.bot.log.info(
                        f'YouTube video "{query}" not found')

                await message.channel.send(
                    embed=SpotifyEmbed(result, message.author))
                await message.channel.send(f'>>> **YouTube**\n{yt}')
                self.bot.log.info(
                    f'Spotify song "{result["name"]}" found on YouTube'
                    f' successfully'
                )
                try:
                    await message.delete()
                except Forbidden or HTTPException or NotFound:
                    pass

    @cog_ext.cog_slash(
        name='autorole',
        description='Aktualizacja ról, dostępne tylko dla Anona.',
        guild_ids=bot_guilds()
    )
    async def autorole(self, ctx: SlashContext):
        if ctx.author.id != 309270832683679745:
            await ctx.send(embed=MissingPermsEmbed())
        else:
            msg = await ctx.send(embed=PleaseWaitEmbed())
            added = 0
            self.bot.log.info(f'Started updating roles by {str(ctx.author)}')
            for member in ctx.guild.members:
                if not member.bot:
                    if await add_basic_roles(ctx.guild, member, ctx.channel):
                        added += 1
            await msg.edit(embed=DoneEmbed(
                f'Zaktualizowana ilość użytkowników: {added}.'
            ))
            self.bot.log.info(f'Updated {added} users')

    @cog_ext.cog_slash(
        name='order',
        description='Daje komuś rangę "order Sashy Grey" żeby pokazać, jak'
                    ' bardzo rucha przeruchane memy.',
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
    async def order(self, ctx: SlashContext, uzytkownik: Member):
        if 641331138622783508 not in map(lambda r: r.id, ctx.author.roles):
            await ctx.send(embed=MissingPermsEmbed())
        elif 799377826859843634 in map(lambda r: r.id, uzytkownik.roles):
            await ctx.send(embed=ErrorEmbed(
                description='Ta osoba już posiada order, ale dodałem jeszcze'
                            ' raz.'
            ))
        else:
            if not (role := ctx.guild.get_role(799377826859843634)):
                return await ctx.message.reply(embed=ErrorEmbed(
                    'Nie znalazłem takiej roli.'
                ))
            try:
                await uzytkownik.add_roles(
                    role,
                    reason='Przeruchanie przeruchanego mema.'
                )
                self.bot.log.info(f'An order was awarded to {str(uzytkownik)}')
            except HTTPException:
                pass
            await ctx.send(embed=DoneEmbed(
                f'{uzytkownik.mention} otrzymał(a) **order Sashy Grey** za'
                f' **przeruchanie przeruchanego mema**.'
            ))


def setup(bot):
    bot.add_cog(Basic(bot))
