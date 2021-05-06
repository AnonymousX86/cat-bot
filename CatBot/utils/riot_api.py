# -*- coding: utf-8 -*-
from json import load as json_load
from os import sep
from typing import List

from requests import get

from CatBot.settings import riot_lol_api

eune_api = 'https://eun1.api.riotgames.com'
europe_api = 'https://europe.api.riotgames.com'
# noinspection SpellCheckingInspection
api_key = riot_lol_api()
headers = {
    'User-Agent': 'Cat bot',
    'X-Riot-Token': api_key
}


def download_champion_json():
    r = get(
        'http://ddragon.leagueoflegends.com/cdn/'
        '11.8.1/data/en_US/champion.json',
        allow_redirects=True
    )
    file_path = f'assets{sep}champion.json'
    try:
        with open(file_path, 'x'):
            pass
    except FileExistsError:
        pass
    with open(file_path, 'wb') as f:
        f.write(r.content)


def champion_id_name(champion_id: int) -> str:
    with open('assets/champion.json') as f:
        champion_data = json_load(f)['data']
    for line_data in champion_data.items():
        if int(line_data[1]['key']) == champion_id:
            return line_data[1]['name']


def champion_maestry(summoner_id: str) -> dict:
    url = '/lol/champion-mastery/v4/champion-masteries/by-summoner/'
    r = get(
        f'{eune_api}{url}{summoner_id}',
        headers=headers
    )
    if r.status_code == 200 and len(r.text) > 2:
        return r.json()
    return {}


class Maestry:
    def __init__(self, name='Nieznany', level: int = 0, points: int = 0):
        self.name = name
        self.level = level
        self.points = points

    @property
    def champion_splash(self) -> str:
        return f'http://ddragon.leagueoflegends.com/cdn/img/champion/' \
               f'loading/{self.name.replace(" ", "")}_0.jpg' \
            if self.name != 'Nieznany' \
            else 'https://dummyimage.com/308x650/000/fff.jpg&text=Brak'


class Match:
    def __init__(self, match_id: str, champion: str, position: str, win: bool):
        self.match_id = match_id
        self.champion = champion
        self.position = position
        self.win = win


def last_matches(puuid: str) -> List[Match]:
    _find_matches = f'/lol/match/v5/matches/by-puuid/{puuid}/ids'
    _inspect_match = f'/lol/match/v5/matches/'
    match_list = []
    counter = -1
    while len(match_list) < 20:
        counter += 1
        r1 = get(
            f'{europe_api}{_find_matches}?start={counter}&count=1',
            headers=headers
        )
        if r1.status_code != 200:
            break
        else:
            match_id = r1.json()[0]
            r2 = get(
                f'{europe_api}{_inspect_match}{match_id}',
                headers=headers
            )
            if r2.status_code != 200:
                break
            else:
                data = r2.json()
                if data['info']['gameMode'] == 'CLASSIC':
                    match_id = data['metadata']['matchId']
                    players: List[dict] = r2.json()['info']['participants']
                    for player in players:
                        if player['puuid'] == puuid:
                            match_list.append(Match(
                                match_id,
                                champion_id_name(player['championId']),
                                player['teamPosition']
                                if player['teamPosition'] != 'UTILITY'
                                else 'SUPPORT',
                                player['win']
                            ))
    return match_list


class Summoner:
    def __init__(self, name: str, matches: bool = False):
        summoner_api = '/lol/summoner/v4/summoners/by-name/'
        league_api = '/lol/league/v4/entries/by-summoner/'

        self.name = name
        self.id = ''
        self.puuid = ''
        self.level = 0
        self.icon_id = 0
        self.maestry = [Maestry()]
        self.matches = []
        self.winrate = 0
        self.position = ''
        self.league = ''
        self.tier = ''
        self.exists = False

        r = get(
            f'{eune_api}{summoner_api}{name}',
            headers=headers
        )
        self.status_code = r.status_code
        if self.status_code == 200:
            data = r.json()
            self.name = data['name']
            self.id = data['id']
            self.puuid = data['puuid']
            self.level = int(data['summonerLevel'])
            self.icon_id = int(data['profileIconId'])
            if maestry_ := champion_maestry(self.id):
                self.maestry = []
                for line_maestry in maestry_:
                    self.maestry.append(Maestry(
                        champion_id_name(line_maestry['championId']),
                        int(line_maestry['championLevel']),
                        int(line_maestry['championPoints']),
                    ))
            if matches:
                self.matches = last_matches(self.puuid)
                try:
                    self.winrate = sum(
                        1 if x.win else 0 for x in self.matches
                    ) * 100 // len(self.matches)
                except ZeroDivisionError:
                    self.winrate = 0
                top_positions = dict()
                for match in self.matches:
                    if (
                            pos := match.position.capitalize()
                    ) not in top_positions:
                        top_positions[pos] = 1
                    else:
                        top_positions[pos] += 1
                if len(top_positions):
                    self.position = max(top_positions, key=top_positions.get)
                    if self.position == 'Middle':
                        self.position = 'Mid'
            r = get(
                f'{eune_api}{league_api}{self.id}',
                headers=headers
            )
            if r.status_code == 200:
                if len(data := r.json()):
                    self.league = data[0]['tier'].capitalize()
                    self.tier = data[0]['rank']
            self.exists = True

    @property
    def icon_url(self) -> str:
        return f'http://ddragon.leagueoflegends.com/cdn/11.8.1/img/' \
               f'profileicon/{self.icon_id}.png'

    @property
    def ranked_position(self) -> str:
        if self.exists and self.position:
            if not (league := self.league):
                league = 'Iron'
            return f'assets/ranked-positions/' \
                   f'Position_{league}-{self.position}.png'
        else:
            return 'https://dummyimage.com/300x300/000/fff.jpg&text=Brak+rangi'
