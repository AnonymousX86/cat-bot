# -*- coding: utf-8 -*-
class Archive:
    def __init__(self, name, link, size):
        self.name = name
        self.link = link
        self.size = size


archives = [
    Archive(
        'Upgraded Survival 1.16.3',
        'http://www.mediafire.com/file/171o6ht045vcz69/UpgradedSurvival_1.16.3.7z/file',
        '544MB'
    )
]
