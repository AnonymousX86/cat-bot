# -*- coding: utf-8 -*-
from logging import basicConfig, INFO

from discord import Game, Status
from discord.ext.commands import Bot, ExtensionNotFound, ExtensionAlreadyLoaded, NoEntryPointError
from nest_asyncio import apply as async_apply

from settings import Settings


def log(prefix: str, text: str):
    """Just prettying print (acting as logging) function"""
    while len(prefix) < 6:
        prefix += ' '
    prefix = f'[{prefix}]'
    print(f'{prefix} {text}')


if __name__ == '__main__':
    async_apply()
    basicConfig(level=INFO)
    bot = Bot(
        command_prefix='ej ',
        description='Private bot.',
        owner_id=309270832683679745
    )


    @bot.event
    async def on_ready():
        log('Bot', 'Logged in as {0} (ID: {0.id})'.format(bot.user))
        await bot.change_presence(status=Status.online, activity=Game(name='z kotami'))

        for cog in [f'CatBot.cogs.{cog}' for cog in [
            'basic'
        ]]:
            p = 'Cogs'
            try:
                bot.load_extension(cog)
                log(p, f'Loaded: {cog}')
            except ExtensionNotFound:
                log(p, f'Not found: {cog}')
            except ExtensionAlreadyLoaded:
                log(p, f'Already loaded: {cog}')
            except NoEntryPointError:
                log(p, f'Extension "{cog}" do not have "setup()" function')
            except Exception as e:
                log(p, f'{e.__class__.__name__}: {e}')

        log('Bot', 'Everything done!')


    bot.run(Settings().bot_token)
