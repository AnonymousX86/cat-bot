# -*- coding: utf-8 -*-
from discord import Member
from discord.ext.commands import Cog, command, Context

from CatBot.embeds.basic import custom_error_em, done_em
from CatBot.utils.database import get_counters, add_counter, add_interrupt, \
    get_interrupts


class Counters(Cog, name='Zliczanie'):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name='liczenie',
        brief='Liczy nasze "counterki"',
        description='Zlicza kiedy...\n'
                    ' - Krystian: jest niecierpliwy,\n'
                    ' - Wojtek: jest leniwy,\n'
                    ' - Marta: narzeka,\n'
                    ' - Anon: informatykuje,\n'
                    ' - Kuba: nie ogarnia,\n'
                    ' - Arras: zmienia zdanie,\n'
                    ' - Agata: wkurza się,\n'
                    ' - Kira: wydaje podejrzane dźwięki,\n'
                    ' - Bezu: psuje metę.',
        aliases=['licz'],
        usage='[użytkownik] [opcja]',
        help='Bez podania użytkownika, podaje Twoje liczniki.\n'
             'Dostępne opcje:\n'
             ' - pokazywanie: brak znaku,\n'
             ' - dodawanie: `+`, `plus`, `dodaj`.'
    )
    async def liczenie(self, ctx: Context, member: Member = None,
                       option: str = None):
        if not member:
            member = ctx.author

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

        if not option:
            c = get_counters(member.id)
            await ctx.send(embed=done_em(
                f'{member.mention} {members[str(member.id)]}'
                f' {c} raz{"" if c == 1 else "y"}.'
            ))
        elif option.lower() in ['+', 'plus', 'dodaj']:
            if not add_counter(member.id):
                await ctx.send(embed=custom_error_em(
                    f'Nie mogę dodać countera {member.mention}'
                ))
            else:
                c = get_counters(member.id)
                await ctx.send(embed=done_em(
                    f'{member.mention} dostał countera,'
                    f' więc {members[str(member.id)]}'
                    f' {c} raz{"" if c == 1 else "y"}.'
                ))
        else:
            await ctx.send(embed=custom_error_em('Błędny argument.'))

    @command(
        name='w_zdanie',
        biref='Zlicza wtrącanie się w zdanie',
        aliases=['w-zdanie', 'przerywanie', 'przerwanie'],
        usage='[użytkownik] [opcja]',
        help='Bez podania użytkownika, podaje Twoje liczniki.\n'
             'Dostępne opcje:\n'
             ' - pokazywanie: brak znaku,\n'
             ' - dodawanie: `+`, `plus`, `dodaj`.'
    )
    async def w_zdanie(self, ctx: Context, member: Member = None,
                       option: str = None):
        if not member:
            member = ctx.author

        if not option:
            n = get_interrupts(member.id)
            await ctx.send(embed=done_em(
                f'{member.mention} przerwał(a) zdanie'
                f' {n} raz{"y" if n != 1 else ""}.'
            ))
        elif option.lower() not in ['+', 'plus', 'dodaj']:
            await ctx.send(embed=custom_error_em('Błędny argument'))
        elif not add_interrupt(member.id):
            await ctx.send(embed=custom_error_em(
                'Wystąpił błąd w zapytaniu do bazy danych.'
            ))
        else:
            n = get_interrupts(member.id)
            await ctx.send(embed=done_em(
                f'{member.mention} znowu przerwał(a) zdanie, czyli zrobił(a)'
                f' to łącznie {n} raz{"y" if n != 1 else ""}.'
            ))


def setup(bot):
    bot.add_cog(Counters(bot))
