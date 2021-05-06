# -*- coding: utf-8 -*-
from CatBot.embeds.core import ErrorEmbed


class MissingSummonerEmbed(ErrorEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.description = 'Nie podałeś(aś) nazwy gracza.'

