from django.shortcuts import render
from database.models import Seasons, Episodes, Tvshows
from django.http import HttpResponse

# Create your views here.
def playlist(path):
    m3ulist = '#EXTM3U\r\n'    
        
    for tvshow in Tvshows.objects.all():
        for episode in Episodes.objects.filter(show_id=tvshow.show_id).order_by('season_id', 'id'):
            m3ulist += '#EXTINF:0 group-title="%s" tvg-logo="%s", %s\r\n' % (tvshow.name, episode.background_image, episode.description)
            m3ulist += '#EXTGRP:%s\r\n' % tvshow.name
            m3ulist += '%s\r\n' % episode.url 
    
    response = HttpResponse(m3ulist, content_type='application/octet-stream')
    return response