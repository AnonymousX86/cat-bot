# -*- coding: utf-8 -*-
from logging import basicConfig, getLogger

from discord import Intents, Embed, Color, Status, Game, ActivityType, Activity
from discord.ext.commands import Bot, ExtensionNotFound, \
    ExtensionAlreadyLoaded, NoEntryPointError, Context, CommandNotFound, \
    MissingPermissions, BotMissingPermissions, UserNotFound, \
    CommandOnCooldown, DisabledCommand
from discord_slash import SlashCommand, SlashContext
from rich.logging import RichHandler

from CatBot.embeds.core import ErrorEmbed, MissingPermissionsEmbed, \
    BotMissingPermissionsEmbed, UserNotFoundEmbed, CommandOnCooldownEmbed, \
    DisabledCommandEmbed
from CatBot.settings import bot_version, bot_token, bot_guilds
from CatBot.utils.riot_api import download_champion_json


def main():
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
        command_prefix='c!',
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
    slash = SlashCommand(bot)

    @bot.event
    async def on_ready():
        log.info('Logged in as "{0}" (ID: {0.id})'.format(bot.user))
        log.info(f'Loaded bot version: "{bot_version()}"')

        await bot.change_presence(
            status=Status.online,
            activity=Activity(
                type=ActivityType.listening,
                name='komend pod /'
            )
        )
        log.info('Updated presence')

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

        await slash.sync_all_commands()

        log.info('Downloading `champion.json`')
        download_champion_json()

        log.info('Everything loaded!')

        bot.log = log

    @slash.slash(
        name='test',
        description='Komenda testowa.',
        guild_ids=bot_guilds()
    )
    async def test(ctx: SlashContext):
        await ctx.send(embeds=[Embed(
            title='Testowy embed',
            color=Color.blurple()
        ), Embed(
            title='Drugi embed',
            color=Color.green()
        )])

    @bot.event
    async def on_command_error(ctx: Context, error: Exception):
        if isinstance(error, CommandNotFound):
            log.warning(
                f'Komenda nie została znaleziona:\n> {ctx.message.content}'
            )
        elif isinstance(error, MissingPermissions):
            await ctx.send(embed=MissingPermissionsEmbed())
        elif isinstance(error, BotMissingPermissions):
            await ctx.send(embed=BotMissingPermissionsEmbed())
        elif isinstance(error, UserNotFound):
            await ctx.send(embed=UserNotFoundEmbed())
        elif isinstance(error, CommandOnCooldown):
            await ctx.send(embed=CommandOnCooldownEmbed())
        elif isinstance(error, DisabledCommand):
            await ctx.send(embed=DisabledCommandEmbed())
        else:
            await ctx.send(embed=ErrorEmbed(
                f'```\n{error.__class__.__name__}: {error}\n```',
                title='Wystąpił nieznany błąd komendy'
            ))

    if not (t := bot_token()):
        log.critical('Brak poprawnych ustawień środowiska')
        try:
            with open('.env') as f:
                content = f.readline()
        except FileNotFoundError:
            log.critical("Brak pliku '.env'")
        else:
            if not content:
                log.critical("Pusty plik '.env'")
            else:
                log.critical('Niepełna konfiguracja')
    else:
        bot.run(t)


if __name__ == '__main__':
    main()
