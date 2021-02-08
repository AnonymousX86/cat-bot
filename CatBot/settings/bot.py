# -*- coding: utf-8 -*-
from . import *


def bot_token() -> str:
    return env.get('BOT_TOKEN')


def bot_version() -> str:
    return env.get('2021.2.2')


def bot_stage() -> str:
    return env.get('STAGE')
