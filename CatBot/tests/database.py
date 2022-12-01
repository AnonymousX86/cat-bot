# -*- coding: utf-8 -*-
"""
Every function is testing the connection with database and verifies database
parity with SQLAlchemy models.
All functions should return None only if an error occurred.
"""
from CatBot.ids.owner import OWNER_ID
from CatBot.utils.database import get_flex, get_counters, get_interrupts, \
    get_bonks


def test_flex():
    assert get_flex(OWNER_ID) is not None


def test_counter():
    assert get_counters(OWNER_ID) is not None


def test_interrupt():
    assert get_interrupts(OWNER_ID) is not None


def test_bonk():
    assert get_bonks(OWNER_ID) is not None
