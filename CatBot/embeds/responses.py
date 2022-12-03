# -*- coding: utf-8 -*-
from socket import gethostbyname, gethostname

from discord import Member

from CatBot.embeds.core import DoneEmbed


class MonologEmbed(DoneEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ':scroll: Skryba kiedyś powiedział...'
        self.description = '*Moim zdaniem to nie ma tak, że dobrze albo że nie' \
                           ' dobrze. Gdybym miał powiedzieć, co cenię w życiu' \
                           ' najbardziej, powiedziałbym, że ludzi. Ekhm... Ludzi,' \
                           ' którzy podali mi pomocną dłoń, kiedy sobie nie radziłem,' \
                           ' kiedy byłem sam. I co ciekawe, to właśnie przypadkowe' \
                           ' spotkania wpływają na nasze życie. Chodzi o to, że kiedy' \
                           ' wyznaje się pewne wartości, nawet pozornie uniwersalne,' \
                           ' bywa, że nie znajduje się zrozumienia, które by tak rzec,' \
                           ' które pomaga się nam rozwijać. Ja miałem szczęście, by' \
                           ' tak rzec, ponieważ je znalazłem. I dziękuję życiu.' \
                           ' Dziękuję mu, życie to śpiew, życie to taniec, życie to' \
                           ' miłość. Wielu ludzi pyta mnie o to samo, ale jak ty to' \
                           ' robisz?, skąd czerpiesz tę radość? A ja odpowiadam, że' \
                           ' to proste, to umiłowanie życia, to właśnie ono sprawia,' \
                           ' że dzisiaj na przykład buduję maszyny, a jutro... kto' \
                           ' wie, dlaczego by nie, oddam się pracy społecznej i będę' \
                           ' ot, choćby sadzić... znaczy... marchew.*'


class IpEmbed(DoneEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = f':information_source: {gethostbyname(gethostname())}'


class PatEmbed(DoneEmbed):
    def __init__(self, member: Member, author: Member, **kwargs):
        super().__init__(**kwargs)
        self.title = f':clap: Pac!'
        self.description = f'{member.mention} został(a) pacnięty(a)' \
                           f' przez {author.mention}.'
        self.set_image(
            url='https://cdn.discordapp.com/attachments/'
                '687040215440949271/860261237866233856/pat.gif'
        )


class HugEmbed(DoneEmbed):
    def __init__(self, member: Member, author: Member, **kwargs):
        super().__init__(**kwargs)
        self.title = ':people_hugging: Przytulas'
        self.description = f'{author.mention} przytulił(a) {member.mention}.'
        self.set_image(
            url='https://cdn.discordapp.com/attachments/'
                '687040215440949271/860261224285339658/hug.gif'
        )


class InsultEmbed(DoneEmbed):
    def __init__(self, insult: str, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Wymyśliłem obelgę'
        self.description = insult
