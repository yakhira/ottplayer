from django.core.management.base import BaseCommand
from collector.views import parse_seasons, parse_episodes, extract_stream, save_episode

class Command(BaseCommand):
    help = 'Parser'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--seasons',
            action='store_true',
            dest='seasons',
            help='Parse seasons',
        )
        
        parser.add_argument(
            '--episodes',
            action='store_true',
            dest='episodes',
            help='Parse episodes',
        )

    def update_seasons(self):
        parse_seasons()

    def update_episodes(self):
        for episode in parse_episodes():
            save_episode(extract_stream(episode))

    def handle(self, *args, **options):
        if options['seasons']:
            self.update_seasons()
        elif options['episodes']:
            self.update_episodes()
