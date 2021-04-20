# -*- coding: utf-8 -*-
from logging import basicConfig, getLogger

from discord import Intents
from discord.ext.commands import Bot, ExtensionNotFound, \
    ExtensionAlreadyLoaded, NoEntryPointError
from rich.logging import RichHandler

from CatBot.settings import bot_version, bot_token

if __name__ == '__main__':
    # noinspection PyArgumentList
    basicConfig(
        level='INFO',
        format='%(message)s',
        datefmt='[%x]',
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    getLogger('sqlalchemy.engine').setLevel('WARNING')
    log = getLogger('rich')
    bot = Bot(
        command_prefix=['ej ', 'Ej ', '<@753541564306948098> '],
        description='Prywatny bot Kociej Rzeszy.',
        owner_id=309270832683679745,
        help_command=None,
        intents=Intents(
            guilds=True,
            members=True,
            presences=True,
            guild_messages=True
        )
    )


    @bot.event
    async def on_ready():
        log.info('Logged in as "{0}" (ID: {0.id})'.format(bot.user))
        log.info(f'Loaded bot version: "{bot_version()}"')

        for cog in [f'CatBot.cogs.{cog}' for cog in [
            'basic', 'bonks', 'counters', 'flexing', 'responses'
        ]]:
            try:
                bot.load_extension(cog)
            except ExtensionNotFound:
                log.warning(f'Not found: {cog}')
            except ExtensionAlreadyLoaded:
                log.warning(f'Already loaded: {cog}')
            except NoEntryPointError:
                log.critical(
                    f'Extension "{cog}" do not have "setup()" function')
            except Exception as e:
                log.critical(f'{e.__class__.__name__}: {e}')
            else:
                log.info(f'Loaded: {cog}')

        log.info('Everything done!')

        bot.log = log


    bot.run(bot_token())
