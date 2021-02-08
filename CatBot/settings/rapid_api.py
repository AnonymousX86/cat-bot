# -*- coding: utf-8 -*-
from . import *


def rapid_api_key() -> str:
    return env.get('RAPIDAPI_KEY')
