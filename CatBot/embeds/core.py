# -*- coding: utf-8 -*-
from datetime import datetime

from discord import Embed, Color


class BaseEmbed(Embed):
    def __init__(self, description: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if title := kwargs.get('title'):
            self.title = title
        if description or (description := kwargs.get('description')):
            self.description = description
        self.timestamp = kwargs.get('timestamp', datetime.utcnow())
        self.color = kwargs.get('color', Color.blurple())


class RedEmbed(BaseEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = Color.red()


class ErrorEmbed(RedEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('title') is None:
            self.title = ':x: Wystąpił błąd'


class MissingPermissionsEmbed(ErrorEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('description') is None:
            self.description = 'Nie możesz tego zrobić. Prawdopodobnie nie' \
                               ' posiadasz odpowiednich uprawnień.'


class BotMissingPermissionsEmbed(ErrorEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('description') is None:
            self.description = 'Nie możesz tego zrobić, Ja (bot) nie posiadam ' \
                               'takich uprawnień.'


class UserNotFoundEmbed(ErrorEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('description') is None:
            self.description = 'Nie mogłem znaleźć takiego użytkownika.'


class CommandOnCooldownEmbed(ErrorEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('description') is None:
            self.description = 'Musisz jeszcze chwilę poczekać aż minie' \
                               ' cooldown komendy.'


class DisabledCommandEmbed(ErrorEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('description') is None:
            self.description = 'Ta komenda jest wyłączona.'


class GreenEmbed(BaseEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = Color.green()


class DoneEmbed(GreenEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('title') is None:
            self.title = ':white_check_mark: Gotowe'


class YellowEmbed(BaseEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = Color.gold()


class PleaseWaitEmbed(YellowEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('title') is None:
            self.title = ':hourglass_flowing_sand: Daj mi chwilę...'


class BlueEmbed(BaseEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = Color.blue()
