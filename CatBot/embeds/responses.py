# -*- coding: utf-8 -*-
from socket import gethostbyname, gethostname

from CatBot.embeds.core import DoneEmbed


class MonologEmbed(DoneEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = ':scroll: Skryba kiedyś powiedział...'
        self.description = '*Moim zdaniem to nie ma tak, że dobrze albo że nie'
        ' dobrze. Gdybym miał powiedzieć, co cenię w życiu'
        ' najbardziej, powiedziałbym, że ludzi. Ekhm... Ludzi,'
        ' którzy podali mi pomocną dłoń, kiedy sobie nie radziłem,'
        ' kiedy byłem sam. I co ciekawe, to właśnie przypadkowe'
        ' spotkania wpływają na nasze życie. Chodzi o to, że kiedy'
        ' wyznaje się pewne wartości, nawet pozornie uniwersalne,'
        ' bywa, że nie znajduje się zrozumienia, które by tak rzec,'
        ' które pomaga się nam rozwijać. Ja miałem szczęście, by'
        ' tak rzec, ponieważ je znalazłem. I dziękuję życiu.'
        ' Dziękuję mu, życie to śpiew, życie to taniec, życie to'
        ' miłość. Wielu ludzi pyta mnie o to samo, ale jak ty to'
        ' robisz?, skąd czerpiesz tę radość? A ja odpowiadam, że'
        ' to proste, to umiłowanie życia, to właśnie ono sprawia,'
        ' że dzisiaj na przykład buduję maszyny, a jutro... kto'
        ' wie, dlaczego by nie, oddam się pracy społecznej i będę'
        ' ot, choćby sadzić... znaczy... marchew.*'


class IpEmbed(DoneEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = f':information_source: {gethostbyname(gethostname())}'
