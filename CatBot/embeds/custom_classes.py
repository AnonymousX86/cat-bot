# -*- coding: utf-8 -*-
from datetime import datetime

from discord import Embed, Color


class BaseEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.timestamp = kwargs['timestamp']
        except KeyError:
            self.timestamp = datetime.utcnow()
        try:
            self.colour = kwargs['color']
        except KeyError:
            self.colour = Color.blurple()


class ErrorEmbed(BaseEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colour = Color.red()


class SuccessEmbed(BaseEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colour = Color.green()
