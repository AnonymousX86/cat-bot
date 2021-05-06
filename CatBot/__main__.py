# -*- coding: utf-8 -*-
from logging import basicConfig, getLogger

from discord import Intents
from discord.ext.commands import Bot, ExtensionNotFound, \
    ExtensionAlreadyLoaded, NoEntryPointError, Context, CommandNotFound, \
    MissingPermissions, BotMissingPermissions, UserNotFound, \
    CommandOnCooldown, DisabledCommand
from rich.logging import RichHandler

from CatBot.embeds.core import ErrorEmbed
from CatBot.settings import bot_version, bot_token
from CatBot.utils.riot_api import download_champion_json

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
        command_prefix=['ej ', 'Ej '],
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
            'basic', 'bonks', 'counters', 'flexing', 'lol', 'responses'
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

        log.info('Downloading `champion.json`')
        download_champion_json()

        log.info('Everything done!')

        bot.log = log


    @bot.event
    async def on_command_error(ctx: Context, error: Exception):
        if isinstance(error, CommandNotFound):
            log.warning(
                f'Komenda nie została znaleziona:\n> {ctx.message.content}'
            )
        elif isinstance(error, MissingPermissions):
            await ctx.send(embed=ErrorEmbed(
                'Nie posiadasz odpowiednich uprawnień'
            ))
        elif isinstance(error, BotMissingPermissions):
            await ctx.send(embed=ErrorEmbed(
                'Ja (bot) nie posiadam takich uprawnień.'
            ))
        elif isinstance(error, UserNotFound):
            await ctx.send(embed=ErrorEmbed(
                'Nie mogłem znaleźć takiego użytkownika.'
            ))
        elif isinstance(error, CommandOnCooldown):
            await ctx.send(embed=ErrorEmbed(
                'Musisz jeszcze chwilę poczekać aż minie cooldown komendy.'
            ))
        elif isinstance(error, DisabledCommand):
            await ctx.send(embed=ErrorEmbed(
                'Ta komenda jest wyłączona.'
            ))
        else:
            await ctx.send(embed=ErrorEmbed(
                f'```\n{error.__class__.__name__}: {error}\n```',
                title='Wystąpił nieznany błąd komendy'
            ))


    bot.run(bot_token())
