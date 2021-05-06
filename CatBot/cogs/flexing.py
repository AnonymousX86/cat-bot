# -*- coding: utf-8 -*-
from discord import User, Member
from discord.ext.commands import Cog, command, Context

from CatBot.embeds.core import MissingMemberEmbed, ErrorEmbed
from CatBot.embeds.flexing import FlexesEmbed, FlextopEmbed, FlexAddedEmbed
from CatBot.utils.database import add_flex, get_flexes, get_top_flexes


class Flexing(Cog, name='Flexowanie'):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='flex',
        brief='Dodaje komuś flex',
        description='Liczenie flexów w celu jakże użytecznych statystyk, kto'
                    ' jest największym flexiarzem.',
        usage='<użytkownik> <powód>'
    )
    async def flex(self, ctx: Context, user: Member = None, *,
                   reason: str = None):
        if not user:
            return await ctx.send(embed=MissingMemberEmbed())
        elif not reason:
            return await ctx.send(embed=ErrorEmbed('Musisz podać powód!'))
        elif ctx.author.id == user.id:
            return await ctx.send(embed=ErrorEmbed(
                'Ziomek, dostajesz flexa za flexa dając flexa i flexując'
                ' siebie... Serio?!'
            ))
        else:
            if not add_flex(user.id, reason):
                return await ctx.message.reply(
                    embed=ErrorEmbed('Nie mogę dodać flexa tej osobie.'))
            else:
                return await ctx.send(embed=FlexAddedEmbed(user, reason))

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
        await ctx.send(embed=FlexesEmbed(user, flexes))

    @command(
        name='flextop',
        brief='Najlepsi flexiarze',
        description='Wysyła listę osób, które najwięcej się flexują.',
        help='Dodatkowy argument pokazuje tylko ostatnie `X` dni.',
        usage='[dni]'
    )
    async def flextop(self, ctx: Context, days: int = 30):
        min_ = 2
        if days < min_:
            return await ctx.send(embed=ErrorEmbed(
                f'Podaj co najmniej {min_}!'
            ))
        flexes = get_top_flexes(days)
        users = [i for i in
                 map(lambda x: ctx.guild.get_member(int(x[0])).mention, flexes)]
        counts = [i for i in map(lambda x: x[1], flexes)]
        await ctx.send(embed=FlextopEmbed(users, counts, days))


def setup(bot):
    bot.add_cog(Flexing(bot))
