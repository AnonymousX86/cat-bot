# -*- coding: utf-8 -*-
from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Settings:
    @property
    def bot_token(self) -> str:
        return getenv("BOT_TOKEN")

    @property
    def bot_version(self) -> str:
        return '0.1.0-alpha'

    @property
    def reddit_client_id(self):
        return getenv('REDDIT_CLIENT_ID')

    @property
    def reddit_client_secret(self):
        return getenv('REDDIT_CLIENT_SECRET')

    @property
    def reddit_user_agent(self):
        return getenv('REDDIT_USER_AGENT').format(self.bot_version)

    @property
    def rapidapi_key(self):
        return getenv('RAPIDAPI_KEY')

    @property
    def spotify_secret(self):
        return getenv('SPOTIFY_SECRET')
