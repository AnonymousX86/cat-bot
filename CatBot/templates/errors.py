# -*- coding: utf-8 -*-
from discord import Embed, Color


def _error_em(text: str, details=None):
    return Embed(
        title=text,
        description=details,
        color=Color.red()
    ) if details else Embed(
        title=text,
        color=Color.red()
    )


def cat_error():
    return _error_em(':no_entry: Koci błąd')


def bad_args_em():
    return _error_em(':passport_control: Co najmniej jeden błędny argument.')


def api_error(details=None):
    return _error_em(':calling: API Error', details)
