from django.core.management.base import BaseCommand
from feed_reader.models import Feed
from feed_reader.utils import update_feed_items

class Command(BaseCommand):
    help = 'Fetch the latest items for all subscribed feeds'

    def handle(self, *args, **kwargs):
        feeds = Feed.objects.all()
        for feed in feeds:
            self.stdout.write(f'Updating feed: {feed.url}')
            try:
                update_feed_items(feed)
            except Exception as e:
                self.stderr.write(f'Error updating {feed.url}: {e}')
        self.stdout.write('Feeds update completed.')
