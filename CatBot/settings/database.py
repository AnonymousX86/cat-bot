# -*- coding: utf-8 -*-
from . import *


def database_url() -> str:
    return env.get('DATABASE_URL')
