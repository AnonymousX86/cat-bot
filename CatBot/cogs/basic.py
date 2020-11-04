# -*- coding: utf-8 -*-
from json import loads
from urllib.parse import quote_plus

import praw
import requests
from discord import Message
from discord.ext.commands import Cog, command, Context

from CatBot.templates.basic import *
from CatBot.templates.errors import *
from settings import Settings


class Basic(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='info'
    )
    async def info(self, ctx):
        await ctx.send(embed=info_em())

    @command(
        name='moneta',
        aliases=['coin', 'coinflip']
    )
    async def coin(self, ctx):
        await ctx.send(embed=coin_em())

    @command(
        name='kot',
        aliases=['kotek', 'koty']
    )
    async def kot(self, ctx):
        msg = await ctx.send(embed=please_wait_em())
        reddit = praw.Reddit(
            client_id=Settings().reddit_client_id,
            client_secret=Settings().reddit_client_secret,
            user_agent=Settings().reddit_user_agent
        )
        sub_name = 'cats'
        to_find = 50
        cats_submissions = reddit.subreddit(sub_name).hot(limit=to_find)
        post_to_pick = randint(1, to_find)
        submission = None
        for i in range(0, post_to_pick):
            submission = next(x for x in cats_submissions if not x.stickied)
        if submission:
            await msg.edit(embed=cat_img_em(sub_name, submission.url))
        else:
            await msg.edit(embed=cat_error())

    @command(
        name='catfact'
    )
    async def catfact(self, ctx, lang='en'):
        if lang not in ['pl', 'en']:
            await ctx.send(embed=bad_args_em())
            return

        response = requests.get('https://cat-fact.herokuapp.com/facts/random')
        if response.status_code != 200:
            await ctx.send(embed=api_error(details='"cat-fact" API'))
            return

        text: str = loads(response.content.decode('UTF-8'))['text']

        if lang != 'en':
            response = requests.request(
                'POST',
                'https://google-translate1.p.rapidapi.com/language/translate/v2',
                data=f'source=en&q={quote_plus(text.encode())}&target={lang}',
                headers={
                    'x-rapidapi-host': 'google-translate1.p.rapidapi.com',
                    'x-rapidapi-key': Settings().rapidapi_key,
                    'accept-encoding': 'application/gzip',
                    'content-type': 'application/x-www-form-urlencoded'
                }
            )
            if response.status_code == 429:
                await ctx.send(embed=api_error(details='API limit reached'))
                return
            elif response.status_code != 200:
                await ctx.send(embed=api_error(details='"google-translate" API'))
                return
            else:
                text: str = loads(response.content.decode('UTF-8'))['data']['translations'][0][0]['translatedText']

        await ctx.send(embed=catfact_em(text))

    @Cog.listener('on_message')
    async def plus_adder(self, message: Message = None):
        if message.channel.id == 773548753428152390:
            await message.add_reaction('👍')
            await message.add_reaction('👎')


def setup(bot):
    bot.add_cog(Basic(bot))
