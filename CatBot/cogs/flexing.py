# -*- coding: utf-8 -*-
from discord import Member, ApplicationContext, user_command, \
    slash_command, Message, Option
from discord.ext.commands import Cog

from CatBot.embeds.core import ErrorEmbed, PleaseWaitEmbed, BlueEmbed, \
    DoneEmbed
from CatBot.embeds.flexing import FlexesEmbed, FlextopEmbed, FlexAddedEmbed
from CatBot.settings import DEFAULT_MEMBER_OPTION
from CatBot.utils.database import get_flexes, get_top_flexes, add_flex


class Flexing(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name='flexy',
        description='Sprawdź ile kto ma flexów'
    )
    async def flex_check(
            self,
            ctx: ApplicationContext,
            member: DEFAULT_MEMBER_OPTION
    ):
        if not member:
            member = ctx.user
        await ctx.send_response(embed=PleaseWaitEmbed())
        await ctx.edit(embed=FlexesEmbed(member, get_flexes(member.id)))

    @user_command(
        name='Flexował Się'
    )
    async def flex_add(
            self,
            ctx: ApplicationContext,
            member: Member
    ):
        if ctx.user.id == member.id:
            await ctx.send_response(embed=ErrorEmbed(
                'Ziomek, dostajesz flexa za flexa dając flexa i flexując siebie... Serio?!'
            ))
            return
        await ctx.send_response(embed=BlueEmbed(
            title=':pencil: Potrzebuję więcej inforamcji',
            description=f'{ctx.user.mention} napisz czym **{member.display_name}**'
                        f' się flexował. *Najlepiej w 3. formie osboowej.*'
                        f' (Tak, po prostu tutaj, na kanale.)'
        ))

        def check(message: Message):
            return message.author.id == ctx.user.id and \
                message.channel.id == ctx.channel_id

        try:
            msg: Message = await self.bot.wait_for(
                'message',
                check=check,
                timeout=240.0
            )
        except TimeoutError:
            await ctx.edit(ErrorEmbed(
                'Następnym razem spróbuj pisać szybciej.'
            ))
            return
        flex_description = msg.content
        await ctx.edit(embed=PleaseWaitEmbed(
            description=f'Dodaję:\n'
                        f'> **{member.mention}** {flex_description}'
        ))
        await msg.delete()
        if not add_flex(member.id, flex_description):
            await ctx.edit(embed=ErrorEmbed(
                'Nie mogę dodać flexa tej osobie.'
            ))
        else:
            await ctx.edit(embed=FlexAddedEmbed(member, flex_description))

    @slash_command(
        name='flextop',
        description='Lista osób, które najwięcej się flexują.'
    )
    async def flextop(
            self,
            ctx: ApplicationContext,
            days: Option(
                int,
                'Z ilu dni mają być pokazane flexy?',
                name='dni',
                min_value=2,
                default=30
            )
    ):
        await ctx.send_response(embed=PleaseWaitEmbed())
        flexes = get_top_flexes(days)
        users = list(filter(
            lambda x: x is not None,
            [i for i in map(lambda x: ctx.guild.get_member(int(x[0])), flexes)]
        ))
        if not users:
            await ctx.edit(embed=DoneEmbed(
                description='Nikt (na razie) nie ma flexów!'
            ))
            return
        counts = [i for i in map(lambda x: x[1], flexes)]
        await ctx.edit(embed=FlextopEmbed(users, counts, days))


def setup(bot):
    bot.add_cog(Flexing(bot))
