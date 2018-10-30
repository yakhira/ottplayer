from django.db import models
from bs4 import BeautifulSoup
import cssutils

class PageParser(object):
    def __init__(self, content):
        self.__soup = BeautifulSoup(content, 'html.parser')
        
    def get_seasons(self, show_id):
        containsSeason = self.__soup.find(itemprop="containsSeason")
        
        if containsSeason:
            children = containsSeason.findChildren(itemprop="url" , recursive=True)
        else:
            return [
                dict(
                    show_id=show_id,
                    season_id=1,
                    url=self.__soup.find("meta",  property="og:url")['content']
                )
            ]
        
        return [
            dict(
                show_id=show_id,
                season_id=child.get_text(), 
                url=child.get('href')
            )
            for child in children
        ]
        

    def get_episodes(self, show_id, season_id):
        episodes = []
        episodesList = self.__soup.find(id="serias-list")
        
        for episode in episodesList:
            if episode.find('div') != -1:
                link = episode.find('div', {'class': 'field-description'}).find('a')
                bg_image_styles = episode.find('div', {'class': 'field-img'})['style']
                background_image = cssutils.parseStyle(bg_image_styles)['background-image']
                background_image_url = background_image.replace('url(', '').replace(')', '')
            
                description = link.get_text().strip().replace('"', "'")

                url = '%s#lostfilm' % link.get('href')
            
                episodes.append(
                    dict(
                        show_id=show_id,
                        season_id=season_id,
                        url=url,
                        background_image=background_image_url,
                        description=description
                    )
                )
            
        return reversed(episodes)
    
    def get_player(self):
        return self.__soup.find(itemprop="embedUrl").get('href')
        
    def get_stream(self, url_id):
        player = self.__soup.find(id='videoplayer%s' % url_id)
        if player:
            return player.get('data-hls')
        return None