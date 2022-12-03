# -*- coding: utf-8 -*-
from discord import ui, ButtonStyle


class EmptyView(ui.View):
    @ui.button(
        label='Czekaj...',
        disabled=True,
        style=ButtonStyle.secondary
    )
    async def _(self):
        pass
