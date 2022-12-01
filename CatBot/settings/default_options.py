# -*- coding: utf-8 -*-
from discord import Option, Member

DEFAULT_MEMBER_OPTION = Option(
    Member,
    'Kogo chcesz sprawdzić?',
    name='użytkownik',
    default=None
)
