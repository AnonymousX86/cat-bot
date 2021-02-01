# -*- coding: utf-8 -*-

from discord import Message, HTTPException, Forbidden, NotFound
from discord.ext.commands import Cog, command, Context
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import SearchVideos

from CatBot.embeds.basic import *
from CatBot.utils.database import add_flex, get_flexes, get_top_flexes


async def add_basic_roles(ctx: Context, member: Member) -> bool:
    for role in map(lambda x: ctx.guild.get_role(x), [718576689302470795, 720650395977777294]):
        try:
            await member.add_roles(role, reason='Automatyzacja ról.')
        except Forbidden:
            await ctx.send(f'Nie mogę dać roli `{role}` użytkownikowi {member.display_name}')
        except HTTPException:
            pass
        else:
            return True
        return False


class Basic(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='info',
        breif='Podstawowe informacje na temat bota',
        description='Pokazuje podstawowe informacje na temat bota. (Na co to komu?)'
    )
    async def info(self, ctx: Context):
        await ctx.send(embed=info_em())

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
                        client_secret=Settings().spotify_secret
                    )
                )
                if not sp:
                    await message.channel.send(embed=custom_error_em('Nie mogę się połączyć ze Spotify!'))
                    await self.bot.log.warning('Can\'t connect to Spotify!')
                    return

                result = sp.track(message.content.split('/')[-1])
                if not result:
                    await message.channel.send(embed=custom_error_em('Błędny link Spotify!'))
                    await self.bot.log.info('Spotify link is wrong!')
                    return

                query = '{} {}'.format(result['name'], ' '.join(map(lambda x: x['name'], result['artists'])))
                # noinspection PyTypeChecker
                yt = SearchVideos(
                    query,
                    mode='dict',
                    max_results=1
                ).result()['search_result'][0]['link']
                if not yt:
                    await message.channel.send(embed=custom_error_em('Wyszukiwanie na YouTube - zawiodło.'))
                    await self.bot.log.info(f'YouTube video "{query}" not found')

                await message.channel.send(embed=spotify_em(result, message.author))
                await message.channel.send(f'>>> **YouTube**\n{yt}')
                self.bot.log.info(f'Spotify song "{result["name"]}" found on YouTube successfully')
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
            await ctx.send(embed=missing_perms_em())
        else:
            msg = await ctx.send(embed=please_wait_em())
            added = 0
            self.bot.log.info(f'Started updating roles by {str(ctx.author)}')
            for member in ctx.guild.members:
                if not member.bot:
                    if await add_basic_roles(ctx, member):
                        added += 1
            await ctx.send(embed=done_em(f'Zaktualizowana ilość ról: {added}.'))
            self.bot.log.info(f'Updated {added} roles')
            await msg.delete()

    # noinspection SpellCheckingInspection
    @command(
        name='order',
        brief='Odznacza kogoś orderem Sashy Grey',
        description='Daje komuś rangę "order Sashy Grey" żeby pokazać, jak bardzo rucha przeruchane memy.'
    )
    async def order(self, ctx: Context, user: Member):
        if not user:
            await ctx.send(embed=missing_user_em())
        elif 641331138622783508 not in map(lambda r: r.id, ctx.author.roles):
            await ctx.send(embed=missing_perms_em())
        elif 799377826859843634 in map(lambda r: r.id, user.roles):
            await ctx.send(embed=custom_error_em('Ta osoba już posiada order, ale dodałem jeszcze raz.'))
        else:
            role = ctx.guild.get_role(799377826859843634)
            if not role:
                return await self.bot.write_and_log('', ctx.channel)
            try:
                await user.add_roles(role, reason='Przeruchanie przeruchanego mema.')
                self.bot.log.info(f'An order was awarder to {str(user)}')
            except HTTPException:
                pass
            await ctx.send(embed=done_em(
                f'{user.mention} otrzymał(a) **order Sashy Grey** za **przeruchanie przeruchanego mema**.'
            ))

    @command(
        name='flex',
        brief='Dodaje komuś flex',
        description='Liczenie flexów w celu jakże użytecznych statystyk, kto jest największym flexiarzem.',
        usage='<użytkownik> <powód>'
    )
    async def flex(self, ctx: Context, user: User, *, reason: str):
        if not user:
            return await ctx.send(embed=missing_user_em())
        elif not reason:
            return await ctx.send(embed=custom_error_em('Musisz podać powód!'))
        else:
            if not add_flex(user.id, reason):
                return await ctx.send(embed=custom_error_em('Nie mogę dodać flexa tej osobie.'))
            else:
                return await ctx.send(embed=done_em(f'{user.mention} dostał(a) flexa za `{reason}`!'))

    @command(
        name='flexy',
        brief='Sprawdza czyjeś flexy',
        description='Pokazuje czyjeś flexy, albo (bez argumentu) Twoje.',
        usage='[użytkownik]'
    )
    async def flexy(self, ctx: Context, user: User = None):
        if not user:
            user = ctx.author
        flexes = get_flexes(user.id)
        await ctx.send(embed=user_flexes_em(user, flexes))

    @command(
        name='flextop',
        brief='Najlepsi flexerzy',
        description='Wysyła listę osób, które najwięcej się flexują.',
        help='[ beta ] Dodatkowy argument pokazuje tylko ostatnie X dni.',
        usage='[dni]'
    )
    async def flextop(self, ctx: Context, days: int = 30):
        min_ = 2
        if days < min_:
            return await ctx.send(embed=custom_error_em(f'Podaj co najmniej {min_}!'))
        flexes = get_top_flexes(days)
        users = [i for i in map(lambda x: ctx.guild.get_member(int(x[0])).mention, flexes)]
        counts = [i for i in map(lambda x: x[1], flexes)]
        await ctx.send(embed=flextop_em(users, counts, days))


def setup(bot):
    bot.add_cog(Basic(bot))
