# -*- coding: utf-8 -*-
from os import environ as env


def bot_token() -> str:
    return env.get('BOT_TOKEN')


def bot_version() -> str:
    return '2021.4.2'


def bot_stage() -> str:
    return env.get('STAGE')
