# -*- coding: utf-8
from os import environ as env


def spotify_secret() -> str:
    return env.get('SPOTIFY_SECRET')
