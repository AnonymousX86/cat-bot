# -*- coding: utf-8 -*-
from asyncio import sleep

from discord import HTTPException, Forbidden, Member, ApplicationContext, \
    user_command, slash_command
from discord.ext.commands import Cog

from CatBot.embeds.basic import InfoEmbed, AutoroleEmbed, RoleAddedEmbed
from CatBot.embeds.core import ErrorEmbed, MissingPermissionsEmbed, \
    PleaseWaitEmbed, \
    DoneEmbed
from CatBot.exceptions import InvalidGuild
from CatBot.ids.channels import ADMINISTRACJA
from CatBot.ids.guilds import KOCIA_RZESZA
from CatBot.ids.roles import JESTEM_Z_IT, ORDER_SASHY_GEY, CZLOWIEKI, \
    BOTELY, PRZYJACIEL
from CatBot.utils.log import log
from CatBot.utils.messages import edit_origin
from CatBot.views.basic import AutoroleView
from CatBot.views.core import EmptyView


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
        if member.guild.id != KOCIA_RZESZA:
            return
        channel = member.guild.get_channel(ADMINISTRACJA)
        if not member.bot:
            normal_role = member.guild.get_role(CZLOWIEKI)
            guest_role = member.guild.get_role(PRZYJACIEL)

            args_pack = (member, normal_role, guest_role)
            await channel.send(
                embed=AutoroleEmbed(*args_pack),
                view=AutoroleView(*args_pack, timeout=None)
            )
        else:
            bot_role = member.guild.get_role(BOTELY)
            try:
                await member.add_roles(bot_role, reason='Automatyzacja ról.')
            except Forbidden:
                await channel.send(embed=ErrorEmbed(
                    f'Nie mogę dać roli {bot_role.mention} botowi {member.mention}.'
                ))
            except HTTPException:
                pass

    @slash_command(
        name='autorole',
        description='Aktualizacja ról, dostępne tylko dla Anona.'
    )
    async def autorole(self, ctx: ApplicationContext):
        if not await self.bot.is_owner(ctx.user):
            await ctx.send_response(embed=MissingPermissionsEmbed())
            return
        await ctx.send_response(embed=PleaseWaitEmbed(
            title='{} Dodawanie ról w trakcie...'.format(
                PleaseWaitEmbed().to_dict().get('title').split(
                    ' ',
                    maxsplit=1
                )[0]
            )
        ))
        added = 0
        normal_role = ctx.guild.get_role(CZLOWIEKI)
        guest_role = ctx.guild.get_role(PRZYJACIEL)
        bot_role = ctx.guild.get_role(BOTELY)
        log.info(f'Started updating roles by {str(ctx.user)}')
        msg = await ctx.send_followup(
            embed=PleaseWaitEmbed(),
            view=EmptyView()
        )
        try:
            for member in sorted(
                    ctx.guild.members,
                    key=lambda m: m.display_name
            ):
                if member.bot:
                    await member.add_roles(bot_role,
                                           reason='Automatyzacja ról.')
                    msg = await msg.edit(
                        embed=DoneEmbed(
                            f'{member.mention} jest botem.'
                        ),
                        view=EmptyView()
                    )
                    await edit_origin(
                        await ctx.channel.fetch_message(
                            msg.reference.message_id
                        ),
                        f'\n:robot: \u2015 {member.mention}'
                    )
                    continue
                elif normal_role in member.roles:
                    msg = await msg.edit(
                        embed=DoneEmbed(
                            f'{member.mention} już posiada rolę {normal_role.mention}'
                        ),
                        view=EmptyView()
                    )
                    await edit_origin(
                        await ctx.channel.fetch_message(
                            msg.reference.message_id
                        ),
                        f'\n:track_next: \u2015 {member.mention}'
                    )
                    continue
                args_pack = (member, normal_role, guest_role)
                msg = await msg.edit(
                    embed=AutoroleEmbed(*args_pack),
                    view=AutoroleView(*args_pack)
                )
                while not (
                        (await ctx.channel.fetch_message(msg.id)).embeds[
                            0].to_dict().get('title') ==
                        DoneEmbed().to_dict().get('title')
                ):
                    await sleep(1)
                msg = await ctx.channel.fetch_message(msg.id)
                if msg.embeds[0].to_dict().get(
                        'description') == RoleAddedEmbed().to_dict().get(
                        'description'):
                    added += 1
            await msg.delete()
        except InvalidGuild:
            await ctx.edit(embed=ErrorEmbed(
                'Dostępne tylko na **Kociej Rzeszy**.'
            ))
            log.warning(f'{ctx.user.name} issued autorole in {ctx.guild.name}')
        else:
            await ctx.edit(embed=DoneEmbed(
                f'Zaktualizowana ilość użytkowników: `{added}`.'
            ))
            log.info(f'Updated {added} users')

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
