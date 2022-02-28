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


class MissingPermissionsEmbed(ErrorEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.description = 'Nie możesz tego zrobić. Prawdopodobnie nie' \
                           ' posiadasz odpowiednich uprawnień.'


class BotMissingPermissionsEmbed(ErrorEmbed):
    def __init__(self):
        super().__init__()
        self.description = 'Nie możesz tego zrobić, Ja (bot) nie posiadam ' \
                           'takich uprawnień.'


class UserNotFoundEmbed(ErrorEmbed):
    def __init__(self):
        super().__init__()
        self.description = 'Nie mogłem znaleźć takiego użytkownika.'


class CommandOnCooldownEmbed(ErrorEmbed):
    def __init__(self):
        super().__init__()
        self.description = 'Musisz jeszcze chwilę poczekać aż minie' \
                           ' cooldown komendy.'


class DisabledCommandEmbed(ErrorEmbed):
    def __init__(self):
        super().__init__()
        self.description = 'Ta komenda jest wyłączona.'


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
