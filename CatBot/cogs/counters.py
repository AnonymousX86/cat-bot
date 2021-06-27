# -*- coding: utf-8 -*-
from discord import Member
from discord.ext.commands import Cog
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from CatBot.embeds.core import DoneEmbed, ErrorEmbed
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
            '358274776806195210': 'nie ogarniał',  # Kuba
            '247711780279681024': 'zmienił zdanie',  # Arras
            '345242327289298946': 'wkurzyła się',  # Agata
            '389092372333723659': 'wydawała dziwne dźwięki',  # Kira
            '157854884668899329': 'psuł metę'  # Bezu
        }

        if not opcja:
            c = get_counters(uzytkownik.id)
            await ctx.send(embed=DoneEmbed(
                f'{uzytkownik.mention} {members[str(uzytkownik.id)]}'
                f' {c} raz{"" if c == 1 else "y"}.'
            ))
        elif opcja.lower() in ['+', 'plus', 'dodaj']:
            if str(uzytkownik.id) not in members.keys():
                await ctx.send(embed=ErrorEmbed(
                    f'{uzytkownik.mention} nie ma counterów.'
                ))
            elif not add_counter(uzytkownik.id):
                await ctx.send(embed=ErrorEmbed(
                    f'Nie mogę dodać countera {uzytkownik.mention}'
                ))
            else:
                c = get_counters(uzytkownik.id)
                await ctx.send(embed=DoneEmbed(
                    f'{uzytkownik.mention} dostał(a) countera,'
                    f' więc {members[str(uzytkownik.id)]}'
                    f' {c} raz{"" if c == 1 else "y"}.'
                ))
        else:
            await ctx.send(embed=ErrorEmbed('Błędny argument.'))

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
            n = get_interrupts(uzytkownik.id)
            await ctx.send(embed=DoneEmbed(
                f'{uzytkownik.mention} przerwał(a) zdanie'
                f' {n} raz{"y" if n != 1 else ""}.'
            ))
        elif opcja.lower() != '+':
            await ctx.send(embed=ErrorEmbed('Błędny argument'))
        elif not add_interrupt(uzytkownik.id):
            await ctx.send(embed=ErrorEmbed(
                'Wystąpił błąd w zapytaniu do bazy danych.'
            ))
        else:
            n = get_interrupts(uzytkownik.id)
            await ctx.send(embed=DoneEmbed(
                f'{uzytkownik.mention} znowu przerwał(a) zdanie, czyli'
                f' zrobił(a) to łącznie {n} raz{"y" if n != 1 else ""}.'
            ))


def setup(bot):
    bot.add_cog(Counters(bot))
