from django.shortcuts import render
from database.models import Tvshows, Seasons, Episodes
from pageparser.models import PageParser

import requests

# Create your views here.
def parse_seasons():
    for tvshow in Tvshows.objects.all():
        response = requests.get(tvshow.url, verify=False)
        if response.status_code == 200:
            parser = PageParser(response.content)
            for season in parser.get_seasons(tvshow.show_id):
                Seasons.objects.update_or_create(
                    url=season['url'],
                    defaults=season
                )

def parse_episodes():
    episodes = []
    
    for tvshow in Tvshows.objects.all():
        seasons = Seasons.objects.filter(show_id=tvshow.show_id).order_by('id')
        last_season = seasons[len(seasons)-1]
        
        for season in seasons:
            if season.season_id != last_season.season_id:
                if Episodes.objects.filter(season=season.season_id):
                    continue
        
            response = requests.get(season.url, verify=False)
            if response.status_code == 200:
                parser = PageParser(response.content)
                episodes.extend(
                    parser.get_episodes(
                        season.show_id,
                        season.season_id
                    )
                )
    
    return episodes

def extract_player(episode):
    response = requests.get(episode['url'], verify=False)
    if response.status_code == 200:
        parser = PageParser(response.content)
        episode['url'] = parser.get_player()
    return episode
    
def extract_stream(episode):
    episode = extract_player(episode)
    response = requests.get(episode['url'], verify=False)
    url_id = episode['url'].split('/')[-1].replace('#', '')

    if response.status_code == 200:
        parser = PageParser(response.content)
        episode['url'] = parser.get_stream(url_id)
    return episode

def save_episode(episode):
    Episodes.objects.update_or_create(
        description=episode['description'],
        defaults=episode
    )