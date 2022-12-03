# -*- coding: utf-8 -*-
from discord import DiscordException


class InvalidGuild(DiscordException):
    """Exception that's raised, when a specific command is available only is specific guild(s)"""
