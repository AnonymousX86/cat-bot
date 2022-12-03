# -*- coding: utf-8 -*-
from logging import basicConfig, getLogger

from discord import Bot, Intents, Status, Activity, ActivityType, \
    ExtensionNotFound, ExtensionAlreadyLoaded, NoEntryPointError, Embed, Color, \
    ApplicationContext, DiscordException, InteractionResponded, \
    ApplicationCommandInvokeError
from discord.ext.commands import MissingPermissions, \
    BotMissingPermissions, UserNotFound, CommandOnCooldown, DisabledCommand
from rich.logging import RichHandler

from .embeds.core import ErrorEmbed, MissingPermissionsEmbed, \
    BotMissingPermissionsEmbed, UserNotFoundEmbed, CommandOnCooldownEmbed, \
    DisabledCommandEmbed, PleaseWaitEmbed, DoneEmbed
from .ids.owner import OWNER_ID
from .settings import bot_version, bot_token, bot_guilds
from .utils.log import log


def main():
    basicConfig(
        level='INFO',
        format='%(message)s',
        datefmt='[%x]',
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    getLogger('sqlalchemy.engine').setLevel('WARNING')
    bot = Bot(
        description='Prywatny bot Kociej Rzeszy.',
        owner_id=OWNER_ID,
        help_command=None,
        auto_sync_commands=False,
        intents=Intents(
            guilds=True,
            guild_messages=True,
            integrations=True,
            members=True,
            message_content=True,
            voice_states=True
        )
    )

    async def sync_command(source: str = None):
        log.info('Commands are syncing...{}'.format(f' ({source})' or ''))
        await bot.sync_commands(guild_ids=bot_guilds())
        log.info('Commands synced')

    async def safe_respond(ctx: ApplicationContext, embed: Embed):
        try:
            await ctx.respond(embed=embed)
        except InteractionResponded or ApplicationCommandInvokeError:
            await ctx.send_followup(embed=embed)

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
            'basic',
            'bonks',
            'counters',
            'flexing',
            'insults',
            'responses'
        ]]:
            try:
                bot.load_extension(cog)
            except ExtensionNotFound:
                log.warning(f'Not found: {cog}')
            except ExtensionAlreadyLoaded:
                log.info(f'Skipping: {cog} (already loaded)')
            except NoEntryPointError:
                log.critical(
                    f'Extension "{cog}" do not have "setup()" function')
            except Exception as e:
                log.critical(f'{e.__class__.__name__}: {e}')
                raise e
            else:
                log.info(f'Loaded: {cog}')

        await sync_command('Initial')

        log.info('Everything loaded!')

    @bot.event
    async def on_application_command_error(
            ctx: ApplicationContext,
            e: DiscordException
    ):
        await ctx.send_followup(embed=ErrorEmbed().add_field(
            name=e.__class__.__name__,
            value=f'```{e}```'
        ))
        raise e

    @bot.slash_command(
        name='test',
        description='Komenda testowa.'
    )
    async def test(ctx: ApplicationContext):
        await ctx.respond(
            embeds=[Embed(
                title='Testowy embed',
                color=Color.blurple()
            ), Embed(
                title='Drugi embed',
                color=Color.green()
            )],
            delete_after=10
        )

    @bot.slash_command(
        name='synchornizacja',
        description='Synchronizuj komendy, też dostepne tylko dla Anona'
    )
    async def cmd_sync(ctx: ApplicationContext):
        if not await bot.is_owner(ctx.user):
            await ctx.respond(embed=MissingPermissionsEmbed())
            return
        await ctx.respond(
            embed=PleaseWaitEmbed(description='Trwa synchronizacja')
        )
        log.info(
            f'Commands are syncing... (In: "{ctx.guild.name} #{ctx.channel}")')
        await sync_command(f'In: "{ctx.guild.name} #{ctx.channel}"')
        await ctx.edit(
            embed=DoneEmbed(description='Komedny zsynchronizowane.'),
            delete_after=10
        )

    @bot.event
    async def on_application_command_error(
            ctx: ApplicationContext,
            error: DiscordException
    ):
        if isinstance(error, MissingPermissions):
            await safe_respond(ctx, MissingPermissionsEmbed())
        elif isinstance(error, BotMissingPermissions):
            await safe_respond(ctx, BotMissingPermissionsEmbed())
        elif isinstance(error, UserNotFound):
            await safe_respond(ctx, UserNotFoundEmbed())
        elif isinstance(error, CommandOnCooldown):
            await safe_respond(ctx, CommandOnCooldownEmbed())
        elif isinstance(error, DisabledCommand):
            await safe_respond(ctx, DisabledCommandEmbed())
        else:
            await safe_respond(ctx, ErrorEmbed(
                title='Wystąpił nieznany błąd komendy',
                description=f'```\n{error.__class__.__name__}: {error}\n```'
            ))
            raise error

    if not (token := bot_token()):
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
        bot.run(token)


if __name__ == '__main__':
    main()
