# -*- coding: utf-8 -*-
from . import *
from .bot import bot_version


def reddit_client_id() -> str:
    return env.get('REDDIT_CLIENT_ID')


def reddit_client_secret() -> str:
    return env.get('REDDIT_CLIENT_SECRET')


def reddit_user_agent() -> str:
    v = env.get('REDDIT_USER_AGENT')
    if v:
        v = v.format(bot_version())
    return v
