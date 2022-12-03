# -*- coding: utf-8 -*-
from discord import ButtonStyle, ui, Member, Role, Forbidden, HTTPException, \
    Interaction, PartialEmoji
from discord.ui import Item, Button

from CatBot.embeds.basic import RoleAddedEmbed
from CatBot.embeds.core import ErrorEmbed, PleaseWaitEmbed, DoneEmbed
from CatBot.utils.messages import edit_origin


class AutoroleView(ui.View):
    normal_emoji = PartialEmoji.from_str('✅')
    guest_emoji = PartialEmoji.from_str('❌')

    def __init__(
            self,
            member: Member,
            normal_role: Role,
            guest_role: Role,
            timeout: float or None = 180,
            *items: Item
    ):
        super().__init__(*items)
        self.member = member
        self.normal_role = normal_role
        self.guest_role = guest_role
        self.timeout = timeout
        self.responded = False

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        if msg := self.message:
            await msg.edit(
                embed=ErrorEmbed(
                    'Następnym razem spróbuj zareagować szybciej!'
                ),
                view=self
            )

    async def button_pressed(
            self,
            button: Button,
            interaction: Interaction
    ):
        await interaction.message.edit(embed=PleaseWaitEmbed())

        applied = False
        role = self.normal_role if button.emoji == self.normal_emoji else self.guest_role
        try:
            if role not in self.member.roles:
                await self.member.add_roles(role)
                if role in self.member.roles:
                    applied = True
                    if role == self.normal_role:
                        await self.member.remove_roles(self.guest_role)
                else:
                    raise Forbidden
        except Forbidden:
            await interaction.response.send_message(
                f'Nie mogę dodać roli `{self.normal_role}` użytkownikowi'
                f' *{self.member.mention}*.',
                delete_after=3
            )
            await edit_origin(
                await interaction.channel.fetch_message(
                    interaction.message.reference.message_id
                ),
                f'\n:warning: \u2015 {self.member.mention}'
            )
        except HTTPException:
            pass
        else:
            await interaction.response.edit_message(
                # Embeds have different descriptions which is used to count
                # real roles added.
                embed=RoleAddedEmbed() if applied else DoneEmbed()
            )

            origin_msg = await interaction.channel.fetch_message(
                interaction.message.reference.message_id
            )
            if origin_msg and origin_msg.embeds[0].to_dict().get(
                    'title') != DoneEmbed().to_dict().get('title'):
                await edit_origin(
                    origin_msg,
                    f'\n{button.emoji} \u2015 {self.member.mention}'
                )

    @ui.button(
        label='Tak',
        style=ButtonStyle.primary,
        emoji=normal_emoji
    )
    async def button_yes(self, button: Button, interaction: Interaction):
        await self.button_pressed(button, interaction)

    @ui.button(
        label='Nie',
        style=ButtonStyle.secondary,
        emoji=guest_emoji
    )
    async def button_no(self, button: Button, interaction: Interaction):
        await self.button_pressed(button, interaction)
