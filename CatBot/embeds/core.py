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


class RedEmbed(BaseEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.colour = kwargs['colour']
        except KeyError:
            self.colour = Color.red()


class ErrorEmbed(RedEmbed):
    def __init__(self, description: str = None, **kwargs):
        super().__init__(**kwargs)
        try:
            self.title = kwargs['title']
        except KeyError:
            self.title = ':x: Wystąpił błąd'
        if description:
            self.description = description


class MissingPermsEmbed(ErrorEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.description = kwargs['description']
        except KeyError:
            self.description = 'Nie możesz tego zrobić. Prawdopodobnie nie' \
                               ' posiadasz odpowiednich uprawnień.'


class MissingMemberEmbed(ErrorEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.description = kwargs['description']
        except KeyError:
            self.description = 'Nie podałeś(aś) użytkownika.'


class GreenEmbed(BaseEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.colour = kwargs['colour']
        except KeyError:
            self.colour = Color.green()


class DoneEmbed(GreenEmbed):
    def __init__(self, description: str = None, **kwargs):
        super().__init__(**kwargs)
        try:
            self.title = kwargs['title']
        except KeyError:
            self.title = ':white_check_mark: Gotowe'
        if description:
            self.description = description


class YellowEmbed(BaseEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.colour = kwargs['colour']
        except KeyError:
            self.colour = Color.gold()


class PleaseWaitEmbed(YellowEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.title = kwargs['title']
        except KeyError:
            self.title = ':hourglass_flowing_sand: Daj mi chwilę...'


class BlueEmbed(BaseEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.colour = kwargs['colour']
        except KeyError:
            self.colour = Color.blue()
