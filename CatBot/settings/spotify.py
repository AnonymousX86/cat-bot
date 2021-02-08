# -*- coding: utf-8
from . import *


def spotify_secret() -> str:
    return env.get('SPOTIFY_SECRET')
