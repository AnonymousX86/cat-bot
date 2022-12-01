# -*- coding: utf-8 -*-
from discord import HTTPException, Forbidden, Guild, \
    TextChannel, Member, ApplicationContext, user_command, slash_command
from discord.ext.commands import Cog

from CatBot.embeds.basic import InfoEmbed
from CatBot.embeds.core import ErrorEmbed, MissingPermissionsEmbed, \
    PleaseWaitEmbed, \
    DoneEmbed
from CatBot.settings import bot_guilds
from CatBot.ids.roles import JESTEM_Z_IT, ORDER_SASHY_GEY, CZLOWIEKI, \
    BOTELY


async def add_basic_roles(guild: Guild, member: Member,
                          channel: TextChannel = None) -> bool:
    success = False
    if not member.bot:
        role = guild.get_role(CZLOWIEKI)
        try:
            await member.add_roles(role, reason='Automatyzacja ról.')
        except Forbidden:
            if channel:
                await channel.send(
                    f'Nie mogę dać roli `{role}` użytkownikowi'
                    f' *{member.display_name}*'
                )
        except HTTPException:
            pass
        else:
            success = True
    else:
        bot_role = guild.get_role(BOTELY)
        try:
            await member.add_roles(bot_role, reason='Automatyzacja ról.')
        except Forbidden:
            if channel:
                await channel.send(
                    f'Nie mogę dać roli botowi *{member.display_name}*'
                )
        except HTTPException:
            pass
        else:
            success = True
    return success


class Basic(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name='info',
        description='Pokazuje podstawowe informacje na temat bota.'
                    ' (Na co to komu?)'
    )
    async def info(self, ctx: ApplicationContext):
        await ctx.send_response(embed=InfoEmbed())

    @Cog.listener('on_member_join')
    async def autorole_updater(self, member: Member):
        await add_basic_roles(member.guild, member)

    @slash_command(
        name='autorole',
        description='Aktualizacja ról, dostępne tylko dla Anona.'
    )
    async def autorole(self, ctx: ApplicationContext):
        if ctx.message.author.id != 309270832683679745:
            await ctx.send_response(embed=MissingPermissionsEmbed())
        else:
            await ctx.send_response(embed=PleaseWaitEmbed())
            added = 0
            self.bot.log.info(f'Started updating roles by {str(ctx.author)}')
            for member in ctx.guild.members:
                if not member.bot:
                    if await add_basic_roles(ctx.guild, member, ctx.channel):
                        added += 1
            await ctx.edit(embed=DoneEmbed(
                f'Zaktualizowana ilość użytkowników: {added}.'
            ))
            self.bot.log.info(f'Updated {added} users')

    @user_command(
        name='Przyznaj Order',
        description='Daje komuś rangę "order Sashy Grey" żeby pokazać, jak'
                    ' bardzo rucha przeruchane memy.'
    )
    async def order(self, ctx: ApplicationContext, member: Member):
        if JESTEM_Z_IT not in map(lambda r: r.id, ctx.message.author.roles):
            await ctx.send_response(embed=MissingPermissionsEmbed())
        elif ORDER_SASHY_GEY in map(lambda r: r.id, member.roles):
            await ctx.send_response(embed=ErrorEmbed(
                description='Ta osoba już posiada order, ale dodałem jeszcze'
                            ' raz.'
            ))
        else:
            if not (role := ctx.guild.get_role(ORDER_SASHY_GEY)):
                return await ctx.message.reply(embed=ErrorEmbed(
                    'Nie znalazłem takiej roli.'
                ))
            try:
                await member.add_roles(
                    role,
                    reason='Przeruchanie przeruchanego mema.'
                )
                self.bot.log.info(f'An order was awarded to {str(member)}')
            except HTTPException:
                pass
            await ctx.send_response(embed=DoneEmbed(
                f'{member.mention} otrzymał(a) **order Sashy Grey** za'
                f' **przeruchanie przeruchanego mema**.'
            ))


def setup(bot):
    bot.add_cog(Basic(bot))
