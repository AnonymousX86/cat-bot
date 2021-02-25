# -*- coding: utf-8 -*-
from discord import User
from discord.ext.commands import Cog, command, Context, cooldown, BucketType, CommandOnCooldown

from CatBot.embeds.basic import missing_user_em, custom_error_em, done_em
from CatBot.embeds.flexing import user_flexes_em, flextop_em
from CatBot.utils.database import add_flex, get_flexes, get_top_flexes


class Flexing(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cooldown(1, 60, BucketType.user)
    @command(
        name='flex',
        brief='Dodaje komuś flex',
        description='Liczenie flexów w celu jakże użytecznych statystyk, kto jest największym flexiarzem.',
        usage='<użytkownik> <powód>'
    )
    async def flex(self, ctx: Context, user: User, *, reason: str):
        if not user:
            return await ctx.message.reply(embed=missing_user_em())
        elif not reason:
            return await ctx.message.reply(embed=custom_error_em('Musisz podać powód!'))
        elif ctx.author.id == user.id:
            return await ctx.message.reply(embed=custom_error_em(
                'Ziomek, dostajesz flexa za flexa dając flexa i flexując siebie... Serio?!'
            ))
        else:
            if not add_flex(user.id, reason):
                return await ctx.message.reply(embed=custom_error_em('Nie mogę dodać flexa tej osobie.'))
            else:
                return await ctx.message.reply(embed=done_em(f'{user.mention} dostał(a) flexa za `{reason}`!'))

    @flex.error
    async def flex_error(self, ctx: Context, error: Exception):
        if isinstance(error, CommandOnCooldown):
            await ctx.message.reply(embed=custom_error_em('Nie bądź taki szybki, poczekaj minutę.'))
        else:
            raise error

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
        await ctx.message.reply(embed=user_flexes_em(user, flexes))

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
            return await ctx.message.reply(embed=custom_error_em(f'Podaj co najmniej {min_}!'))
        flexes = get_top_flexes(days)
        users = [i for i in map(lambda x: ctx.guild.get_member(int(x[0])).mention, flexes)]
        counts = [i for i in map(lambda x: x[1], flexes)]
        await ctx.message.reply(embed=flextop_em(users, counts, days))


def setup(bot):
    bot.add_cog(Flexing(bot))
