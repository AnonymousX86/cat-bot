# -*- coding: utf-8 -*-
from typing import Optional, Tuple, List

from mcstatus import MinecraftServer
from mcstatus.pinger import PingResponse


class Archive:
    def __init__(self, name, link, size):
        self.name = name
        self.link = link
        self.size = size


def archives() -> List[Archive]:
    return [
        Archive(
            'Upgraded Survival 1.16.3',
            'http://www.mediafire.com/file/171o6ht045vcz69/UpgradedSurvival_1.16.3.7z/file',
            '544MB'
        )
    ]


def server_status() -> Tuple[Optional[PingResponse], Optional[BaseException]]:
    try:
        return MinecraftServer.lookup('vmi472388.contaboserver.net').status(), None
    except BaseException as e:
        return None, e
