# -*- coding: utf-8 -*-
from os import environ as env


def rapid_api_key() -> str:
    return env.get('RAPIDAPI_KEY')
