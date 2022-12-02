# -*- coding: utf-8 -*-
from os import environ as env

from CatBot.ids.guilds import KOCIA_RZESZA, ANONYMOUS_BOTS


def bot_token() -> str:
    return env.get('BOT_TOKEN')


def bot_version() -> str:
    return '2022.12.7'


def bot_stage() -> str:
    return env.get('STAGE', 'unknown')


def bot_guilds() -> list[int]:
    return [KOCIA_RZESZA, ANONYMOUS_BOTS]


def dev_guilds() -> list[int]:
    return [ANONYMOUS_BOTS]
