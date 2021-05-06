# -*- coding: utf-8 -*-
from discord import File
from discord.ext.commands import Cog, command, Context, cooldown, BucketType
from requests import get

from CatBot.embeds.core import ErrorEmbed, PleaseWaitEmbed, DoneEmbed
from CatBot.embeds.lol import MissingSummonerEmbed
from CatBot.utils.riot_api import Summoner


class Lol(Cog, name='LoL'):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='status',
        brief='Status serwerów LoL'
    )
    async def status(self, ctx: Context):
        # noinspection SpellCheckingInspection
        r = get(
            'https://eun1.api.riotgames.com/lol/status/v3/shard-data',
            headers={
                'User-Agent': 'Cat bot',
                'X-Riot-Token': 'RGAPI-8c83885b-36f0-4f4a-9251-c3e03892059d'
            }
        )
        await ctx.send(embed=DoneEmbed(
            title='API response',
            description=f'Code: {r.status_code}'
        ).add_field(
            name='Text',
            value=str(r.content.decode('utf-8'))[:500] + '...'
        ))

    @cooldown(1, 8, BucketType.guild)
    @command(
        name='summoner',
        brief='Informacje o graczu',
        description='Pokazuje poziom przywoływacza, awatar i najwyższą'
                    ' maestrię.',
        usage='<nazwa gracza> [dodatkowe opcje]',
        help='Dodatkowe opcje:\n'
             '-ids  -  pokazuje ID i PUUID'
    )
    async def summoner(self, ctx: Context, name: str = None, *,
                       options: str = ''):
        if not name:
            return await ctx.send(embed=MissingSummonerEmbed())
        msg = await ctx.send(embed=PleaseWaitEmbed())
        player = Summoner(name)
        if player.exists:
            em = DoneEmbed(
                title=player.name
            ).add_field(
                name='Poziom',
                value=str(player.level),
                inline=False
            ).set_thumbnail(
                url=player.icon_url
            )
            if '-ids' in options:
                em.add_field(
                    name='Summoner ID',
                    value=f'```\n{player.id}\n```',
                    inline=False
                ).add_field(
                    name='PUUID',
                    value=f'```\n{player.puuid}\n```',
                    inline=False
                )
            if 'debug' in options:
                em.add_field(
                    name='Debug',
                    value=str(player.matches)[1000]
                )
            em.add_field(
                name='Najwyższa maestria',
                value=player.maestry[0].name,
                inline=False
            ).add_field(
                name='Poziom',
                value=str(player.maestry[0].level)
            ).add_field(
                name='Punkty',
                value=str(player.maestry[0].points)
            )
            if player.maestry[0].name != 'Nieznany':
                em.set_image(url=player.maestry[0].champion_splash)
            await msg.edit(embed=em)
        elif str((c := player.status_code)).startswith('4'):
            await msg.edit(embed=ErrorEmbed(
                f'Gracz `{name}` nie istnieje na EUNE.'
            ))
        else:
            await msg.edit(embed=ErrorEmbed(
                f'Wystąpił błąd: `{c}`.'
            ))

    @cooldown(1, 8, BucketType.guild)
    @command(
        name='maestria',
        aliases=['maestry'],
        usage='<nazwa gracza> [liczba bohaterów]',
        help='Maksymalną liczbą bohaterów jest 25.'
    )
    async def maestria(self, ctx: Context, name: str = None, count: int = 6):
        if not name:
            return await ctx.send(embed=MissingSummonerEmbed())
        elif count > 25:
            count = 25
        msg = await ctx.send(embed=PleaseWaitEmbed())
        player = Summoner(name, matches=True)
        if not player.exists:
            em = ErrorEmbed(f'Gracz `{name}` nie istnieje na EUNE.')
        else:
            maestry = player.maestry[:count]
            if not (n := len(maestry)):
                em = ErrorEmbed(
                    f'Gracz `{player.name}` nie posiada maestrii na EUNE.'
                )
            else:
                em = DoneEmbed(
                    title=player.name,
                    description=f'Top {n} maestrii'
                )
                for m in maestry:
                    em.add_field(
                        name=m.name,
                        value=f'**Poziom** {m.level}\n'
                              f'**Pkt** {m.points}'
                    )
            em.set_thumbnail(
                url=player.icon_url
            )
        await msg.edit(embed=em)

    @cooldown(1, 8, BucketType.guild)
    @command(
        name='winrate',
        aliases=['wr'],
        usage='<nazwa gracza>'
    )
    async def winrate(self, ctx: Context, name: str = None):
        if not name:
            await ctx.send(embed=MissingSummonerEmbed())
        else:
            msg = await ctx.send(embed=PleaseWaitEmbed())
            if not (player := Summoner(name, matches=True)).exists:
                await msg.edit(embed=ErrorEmbed(
                    f'Gracz `{name}` nie istnieje na EUNE.'
                ))
            else:
                em = DoneEmbed(
                    title=player.name,
                    description=f'Procent wygranych: **{player.winrate}%**'
                                f' *({sum(m.win for m in player.matches)}/'
                                f'{len(player.matches)})*.'
                ).add_field(
                    name='Historia',
                    value='Najnowsze \u2192 najstarsze\n' + '\n'.join(map(
                        lambda x: (
                                      ":green_square:"
                                      if x.win
                                      else ":red_square:"
                                  ) + f' **{x.champion}**'
                                      f' {x.position.capitalize()}',
                        player.matches
                    ))
                )
                if player.league:
                    em.add_field(
                        name='Ranga',
                        value=f'{player.league} {player.tier}'
                    )
                if (img := player.ranked_position).startswith('http'):
                    em.set_thumbnail(url=img)
                else:
                    with open(img, 'rb') as f:
                        foo_msg = await self.bot.get_channel(
                            687040215440949271
                        ).send(file=File(f))
                    em.set_thumbnail(url=foo_msg.attachments[0].url)
                await msg.edit(embed=em)


def setup(bot):
    bot.add_cog(Lol(bot))
