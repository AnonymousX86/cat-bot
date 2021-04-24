# -*- coding: utf-8 -*-
from os import environ as env


def riot_lol_api() -> str:
    return env.get('RIOT_LOL_API')

