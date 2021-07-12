# -*- coding: utf-8 -*-
from os import environ as env
from typing import List


def bot_token() -> str:
    return env.get('BOT_TOKEN')


def bot_version() -> str:
    return '2021.7.2'


def bot_stage() -> str:
    return env.get('STAGE')


def bot_guilds() -> List[int]:
    return [385122529343176705, 670766319372599297]


def dev_guild() -> List[int]:
    return [670766319372599297]
