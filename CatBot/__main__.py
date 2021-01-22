# -*- coding: utf-8 -*-
from logging import basicConfig, getLogger

from discord import Intents
from discord.ext.commands import Bot, ExtensionNotFound, ExtensionAlreadyLoaded, NoEntryPointError
from nest_asyncio import apply as async_apply
from rich.logging import RichHandler

from settings import Settings

if __name__ == '__main__':
    async_apply()
    basicConfig(
        level='INFO',
        format='%(message)s',
        datefmt='[%x]',
        handlers=[RichHandler()]
    )
    log = getLogger('rich')
    bot = Bot(
        command_prefix=['ej ', 'Ej ', '<@753541564306948098> '],
        description='Private bot.',
        owner_id=309270832683679745,
        intents=Intents(
            guilds=True,
            members=True,
            guild_messages=True
        )
    )


    @bot.event
    async def on_ready():
        log.info('Logged in as {0} (ID: {0.id})'.format(bot.user))

        for cog in [f'CatBot.cogs.{cog}' for cog in ['basic']]:
            try:
                bot.load_extension(cog)
            except ExtensionNotFound:
                log.warning(f'Not found: {cog}')
            except ExtensionAlreadyLoaded:
                log.warning(f'Already loaded: {cog}')
            except NoEntryPointError:
                log.warning(f'Extension "{cog}" do not have "setup()" function')
            except Exception as e:
                log.warning(f'{e.__class__.__name__}: {e}')
            else:
                log.info(f'Loaded: {cog}')

        log.info('Everything done!')


    bot.run(Settings().bot_token)
