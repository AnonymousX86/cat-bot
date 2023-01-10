# -*- coding: utf-8 -*-
from datetime import datetime

from CatBot.embeds.core import GreenEmbed


class KebabEmbed(GreenEmbed):
    def __init__(
            self,
            user_name: str,
            kebab_date: datetime,
            kebab_description: str = None,
            kebab_picture_url: str = None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.title = f'**{user_name}** dodał(a) kebsa'
        self.description = '{}{}'.format(
            (kebab_description + '\n\n') if kebab_description else '',
            f'<t:{int(datetime.timestamp(kebab_date))}:d>'
        )
        if kebab_picture_url.startswith('http'):
            self.set_image(url=kebab_picture_url)
