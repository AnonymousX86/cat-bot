# -*- coding: utf-8 -*-
from socket import timeout
from typing import Optional

from mcstatus import MinecraftServer
from mcstatus.pinger import PingResponse


class Archive:
    def __init__(self, name, link, size):
        self.name = name
        self.link = link
        self.size = size


def archives():
    return [
        Archive(
            'Upgraded Survival 1.16.3',
            'http://www.mediafire.com/file/171o6ht045vcz69/UpgradedSurvival_1.16.3.7z/file',
            '544MB'
        )
    ]


def server_status() -> Optional[PingResponse]:
    try:
        return MinecraftServer.lookup('kociaki.tasrv.com').status()
    except timeout:
        return None
