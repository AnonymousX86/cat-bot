# -*- coding: utf-8 -*-
from discord import Embed, Message


async def edit_origin(origin_message: Message, text: str):
    embed_copy = origin_message.embeds[0].copy()
    if embed_copy.description is Embed.Empty:
        embed_copy.description = ''
    embed_copy.description += text
    await origin_message.edit(
        embed=embed_copy
    )
