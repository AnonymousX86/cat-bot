# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from discord import Bot, slash_command, ApplicationContext, Option, TextChannel, File, Message
from discord.ext.commands import Cog
from sqlalchemy.util import timezone

from CatBot.embeds.core import PleaseWaitEmbed, DoneEmbed, ErrorEmbed
from CatBot.embeds.kebab_counter import KebabEmbed
from CatBot.ids.channels import KEBAB_COUNTER, MEDIA
from CatBot.ids.guilds import ANONYMOUS_BOTS
from CatBot.utils.database import add_kebab


class KebabCounter(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(
        name='kebab',
        description='Pochwal się swoim kebabem. Dodaj zdjęcie wysyłając je przed użyciem tej komendy'
    )
    async def kebab(
            self,
            ctx: ApplicationContext,
            kebab_description: Option(
                str,
                'Jakiego kebsa jadłeś(aś)?',
                name='opis',
                required=True
            ),
            kebab_date: Option(
                str,
                'Kiedy jadłeś tego kebsa? Format: RRRRR-MM-DD Domyślnie dzisiaj',
                name='data',
                default=None
            )
    ):
        await ctx.respond(embed=PleaseWaitEmbed(), ephemeral=True)

        if kebab_date is None:
            kebab_date = datetime.now(tz=timezone(offset=timedelta(hours=1), name='Europe/Warsaw'))
        else:
            try:
                kebab_date = datetime.fromisoformat(kebab_date)
            except ValueError:
                kebab_date = datetime.utcnow()

        kebab_picture_url = ''
        img_msg = None
        async for msg in ctx.channel.history(limit=5):
            if msg.author.id == ctx.user.id:
                if atts := msg.attachments:
                    if (img := atts[0]).content_type.startswith('image/'):
                        kebab_picture = await img.to_file()
                        dev_guild = await self.bot.fetch_guild(ANONYMOUS_BOTS)
                        media_channel: TextChannel = await dev_guild.fetch_channel(MEDIA)
                        if isinstance(kebab_picture, File):
                            new_msg = await media_channel.send(file=kebab_picture)
                            kebab_picture_url = new_msg.attachments[0].proxy_url
                        img_msg = msg
                        break

        new_kebab = add_kebab(
            user_id=ctx.user.id,
            kebab_date=kebab_date,
            kebab_description=kebab_description,
            kebab_picture_url=kebab_picture_url
        )

        kebab_channel: TextChannel = await ctx.guild.fetch_channel(KEBAB_COUNTER)
        kebab_msg = await kebab_channel.send(embed=KebabEmbed(
            user_name=ctx.user.display_name,
            kebab_date=kebab_date,
            kebab_description=kebab_description,
            kebab_picture_url=kebab_picture_url
        ))

        if new_kebab is None:
            await ctx.interaction.edit_original_response(embed=ErrorEmbed(
                'Kebab nie został dodany.'
            ))
        else:
            await ctx.interaction.edit_original_response(embed=DoneEmbed(
                f'Kebab dodany - zobacz [tutaj]({kebab_msg.jump_url})'
            ))

        if isinstance(img_msg, Message):
            await img_msg.delete(delay=10, reason=f'{ctx.user.name} dodał(a) kebsa')


def setup(bot: Bot):
    bot.add_cog(KebabCounter(bot))
