# -*- coding: utf-8 -*-
from discord import Message, HTTPException, Forbidden, NotFound, Guild, \
    TextChannel, Member
from discord.ext.commands import Cog, command, Context
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import SearchVideos

from CatBot.embeds.basic import InfoEmbed, SpotifyEmbed
from CatBot.embeds.core import ErrorEmbed, MissingPermsEmbed, PleaseWaitEmbed, \
    DoneEmbed, MissingMemberEmbed, GreenEmbed
from CatBot.settings import spotify_secret


async def add_basic_roles(guild: Guild, member: Member,
                          channel: TextChannel = None) -> bool:
    result = False
    for role in map(lambda x: guild.get_role(x),
                    [718576689302470795, 720650395977777294]):
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
            result = True
    return result


class Basic(Cog, name='Podstawowe'):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='help',
        brief='Pokazuje to okno',
        description='Możesz wyświetlić pomoc dla kategorii lub komendy.'
    )
    async def help(self, ctx: Context, arg: str = None):
        if not arg:
            em = GreenEmbed(title='Wszystkie dostępne komendy.')
            for cog in self.bot.cogs:
                em.add_field(
                    name=cog,
                    value='\n'.join(
                        f'`{x.name}` - {x.brief or "Brak opisu"}'
                        for x in self.bot.cogs[cog].get_commands()
                    ),
                    inline=False
                )
            await ctx.send(embed=em)
        elif cog := self.bot.get_cog(arg.capitalize()):
            await ctx.send(embed=GreenEmbed(
                title=cog.qualified_name,
                description=cog.description
            ).add_field(
                name='Dostępne komendy',
                value='\n'.join(f'- `{x.name}`' for x in cog.get_commands())
            ))
        elif cmd := self.bot.get_command(arg):
            await ctx.send(embed=GreenEmbed(
                title=cmd.name,
                description=cmd.description
            ).add_field(
                name='Aliasy',
                value=', '.join(f'`{x}`' for x in cmd.aliases) or 'Brak',
                inline=False
            ).add_field(
                name='Używanie',
                value=f'```\n{ctx.prefix}{cmd.name} {cmd.usage or ""}\n```',
                inline=False
            ).add_field(
                name='Pomoc',
                value=f'```\n{cmd.help}\n```' if cmd.help else "Brak",
                inline=False
            ))
        else:
            await ctx.send(embed=ErrorEmbed(
                description='Nie znalazłem takiej komendy ani kategorii'
            ))

    @command(
        name='info',
        brief='Podstawowe informacje na temat bota',
        description='Pokazuje podstawowe informacje na temat bota.'
                    ' (Na co to komu?)'
    )
    async def info(self, ctx: Context):
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

    @command(
        name='autorole',
        biref='Aktualizacja ról',
        description='Dostępne tylko dla Anona.',
        hidden=True
    )
    async def autorole(self, ctx: Context):
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

    # noinspection SpellCheckingInspection
    @command(
        name='order',
        brief='Odznacza kogoś orderem Sashy Grey',
        description='Daje komuś rangę "order Sashy Grey" żeby pokazać, jak'
                    ' bardzo rucha przeruchane memy.'
    )
    async def order(self, ctx: Context, user: Member):
        if not user:
            await ctx.send(embed=MissingMemberEmbed())
        elif 641331138622783508 not in map(lambda r: r.id, ctx.author.roles):
            await ctx.send(embed=MissingPermsEmbed())
        elif 799377826859843634 in map(lambda r: r.id, user.roles):
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
                await user.add_roles(
                    role,
                    reason='Przeruchanie przeruchanego mema.'
                )
                self.bot.log.info(f'An order was awarded to {str(user)}')
            except HTTPException:
                pass
            await ctx.send(embed=DoneEmbed(
                f'{user.mention} otrzymał(a) **order Sashy Grey** za'
                f' **przeruchanie przeruchanego mema**.'
            ))


def setup(bot):
    bot.add_cog(Basic(bot))
