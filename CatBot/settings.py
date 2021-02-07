# -*- coding: utf-8 -*-
from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Settings:
    @property
    def bot_version(self) -> str:
        return '2021.2.2'

    @property
    def bot_token(self) -> str:
        return getenv('BOT_TOKEN')

    @property
    def bot_stage(self) -> str:
        return getenv('STAGE')

    @property
    def reddit_client_id(self) -> str:
        return getenv('REDDIT_CLIENT_ID')

    @property
    def reddit_client_secret(self) -> str:
        return getenv('REDDIT_CLIENT_SECRET')

    @property
    def reddit_user_agent(self) -> str:
        return getenv('REDDIT_USER_AGENT')

    @property
    def rapidapi_key(self) -> str:
        return getenv('RAPIDAPI_KEY')

    @property
    def spotify_secret(self) -> str:
        return getenv('SPOTIFY_SECRET')

    @property
    def database_url(self) -> str:
        return getenv('DATABASE_URL')
