# -*- coding: utf-8 -*-
from discord import Member
from discord.ext.commands import Cog, command, Context, cooldown, BucketType

from CatBot.embeds.basic import custom_error_em, done_em
from CatBot.utils.database import get_counters, add_counter


class Counters(Cog, name='Zliczanie'):
    def __init__(self, bot):
        self.bot = bot

    @cooldown(3, 60, BucketType.guild)
    @command(
        name='liczenie',
        description='Zlicza kiedy...\n'
                    ' - Krystian: jest niecierpliwy,\n'
                    ' - Wojtek: jest leniwy,\n'
                    ' - Marta: narzeka,\n'
                    ' - Anon: informatykuje,\n'
                    ' - Kuba: nie ogarnia,\n'
                    ' - Arras: przerywa zdanie,\n'
                    ' - Agata: wkurza się,\n'
                    ' - Kira: wydaje podejrzane dźwięki,\n'
                    ' - Bezu: psuje metę.',
        aliases=['licz'],
        usage='[użytkownik] [opcja]',
        help='Dostępne opcje:\n'
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
            '309270832683679745': 'informatykował',  # Kuba S.
            '358274776806195210': 'nie ogarniał',  # Kuba K.
            '247711780279681024': 'przerwał zdanie',  # Arras
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


def setup(bot):
    bot.add_cog(Counters(bot))
