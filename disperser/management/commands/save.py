import os
from django.core.management.base import BaseCommand
from collector.views import parse_seasons, parse_episodes, extract_stream, save_episode
from disperser.views import push_playlist
from ottplayer.settings import REPOSITORY, PATH

class Command(BaseCommand):
    help = 'Parser'
    
    def handle(self, *args, **options):
        os.chmod(SSH_KEY_FILE, 0o600)
        push_playlist(REPOSITORY, PATH)
