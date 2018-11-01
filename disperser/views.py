from django.shortcuts import render
from database.models import Seasons, Episodes, Tvshows
from disperser.models import GitHub

# Create your views here.
def push_playlist(repository, path):
    playlist_file = '%s/playlist.m3u8' % path
    m3ulist = '#EXTM3U\r\n'    
        
    for tvshow in Tvshows.objects.all():
        for episode in Episodes.objects.filter(show_id=tvshow.show_id).order_by('season_id', 'id'):
            m3ulist += '#EXTINF:0 group-title="%s" tvg-logo="%s", %s\r\n' % (tvshow.name, episode.background_image, episode.description)
            m3ulist += '#EXTGRP:%s\r\n' % tvshow.name
            m3ulist += '%s\r\n' % episode.url 
    
    repo = GitHub(repository, path)
    repo.pull()
    
    with open(playlist_file, 'w') as infile:
        infile.write(m3ulist)
    
    repo.add(playlist_file)
    repo.push()
        
    return m3ulist