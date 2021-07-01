# -*- coding: utf-8 -*-
from discord import Member
from discord.ext.commands import Cog
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from CatBot.embeds.core import ErrorEmbed
from CatBot.embeds.counters import CounterAddedEmbed, CountersEmbed, \
    InterruptsEmbed, InterruptAddedEmbed
from CatBot.settings import bot_guilds
from CatBot.utils.database import get_counters, add_counter, add_interrupt, \
    get_interrupts


class Counters(Cog, name='Zliczanie'):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='licz',
        description='Liczy nasze "counterki"',
        guild_ids=bot_guilds(),
        options=[
            create_option(
                name='uzytkownik',
                description='Wybierz kogoś z serwera. Jeżeli nie - bot wybierze'
                            ' Ciebie.',
                option_type=6,
                required=False
            ),
            create_option(
                name='opcja',
                description='Sprawdzenie counterów lub dodanie kolejnego.',
                option_type=3,
                required=False,
                choices=[
                    create_choice(
                        name='Zobacz ilość counterów.',
                        value=''
                    ),
                    create_choice(
                        name='Dodaj counter.',
                        value='+'
                    )
                ]
            )
        ]
    )
    async def licz(self, ctx: SlashContext, uzytkownik: Member = None,
                   opcja: str = None):
        if not uzytkownik:
            uzytkownik = ctx.author

        members = {
            '220560592555999232': 'był niecierpliwy',  # Krystian
            '662713379416178690': 'był leniwy',  # Wojtek
            '560826194824790056': 'narzekała',  # Marta
            '309270832683679745': 'informatykował',  # Anon
            # TODO do zmiany (?)
            '358274776806195210': 'nie ogarniał',  # Kuba
            '247711780279681024': 'zmienił zdanie',  # Arras
            '345242327289298946': 'wkurzyła się',  # Agata
            '389092372333723659': 'wydawała dziwne dźwięki',  # Kira
            '157854884668899329': 'psuł metę'  # Bezu
        }

        if not opcja:
            await ctx.send(embed=CountersEmbed(
                uzytkownik,
                members[str(uzytkownik.id)],
                get_counters(uzytkownik.id)
            ))
        elif opcja != '+':
            await ctx.send(embed=ErrorEmbed('Błędny argument.'))
        else:
            if str(uzytkownik.id) not in members.keys():
                await ctx.send(embed=ErrorEmbed(
                    f'{uzytkownik.mention} nie ma counterów.'
                ))
            elif not add_counter(uzytkownik.id):
                await ctx.send(embed=ErrorEmbed(
                    f'Nie mogę dodać countera {uzytkownik.mention}'
                ))
            else:
                await ctx.send(embed=CounterAddedEmbed(
                    uzytkownik,
                    members[str(uzytkownik.id)],
                    get_counters(uzytkownik.id)
                ))

    @cog_ext.cog_slash(
        name='w_zdanie',
        description='Zlicza wtrącanie się w zdanie',
        guild_ids=bot_guilds(),
        options=[
            create_option(
                name='uzytkownik',
                description='Wybierz kogoś z serwera. Jeżeli nie - bot wybierze'
                            ' Ciebie.',
                option_type=6,
                required=False
            ),
            create_option(
                name='opcja',
                description='Możesz zobaczyć wartość lub dodać licznik.',
                option_type=3,
                required=False,
                choices=[
                    create_choice(
                        name='Zobacz wartość',
                        value=''
                    ),
                    create_choice(
                        name='Dodaj +1',
                        value='+'
                    )
                ]
            )
        ]
    )
    async def w_zdanie(self, ctx: SlashContext, uzytkownik: Member = None,
                       opcja: str = None):
        if not uzytkownik:
            uzytkownik = ctx.author

        if not opcja:
            await ctx.send(embed=InterruptsEmbed(
                uzytkownik,
                get_interrupts(uzytkownik.id)
            ))
        elif opcja.lower() != '+':
            await ctx.send(embed=ErrorEmbed('Błędny argument'))
        elif not add_interrupt(uzytkownik.id):
            await ctx.send(embed=ErrorEmbed(
                'Wystąpił błąd w zapytaniu do bazy danych.'
            ))
        else:
            await ctx.send(embed=InterruptAddedEmbed(
                uzytkownik,
                get_interrupts(uzytkownik.id)
            ))


def setup(bot):
    bot.add_cog(Counters(bot))
