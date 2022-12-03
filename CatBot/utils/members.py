# -*- coding: utf-8 -*-
from datetime import datetime
from random import choice, Random

from discord import Member, User


class CustomRandom(Random):
    def __init__(self, seed=datetime.now().strftime('%Y%m%d').encode('utf-8')):
        super().__init__(seed)


def random_member(members: list[Member | User], *, random_per_day=False):
    func = CustomRandom().choice if random_per_day else choice
    return func(list(filter(lambda x: x.bot is False, members)))
