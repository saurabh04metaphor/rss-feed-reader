import feedparser
from datetime import datetime
from django.utils.timezone import make_aware
from .models import Feed, FeedItem

def update_feed_items(feed: Feed):
    """
    Fetch and parse RSS feed items from feed.url, add new FeedItem objects to database.
    """
    parsed_feed = feedparser.parse(feed.url)
    
    # Update feed title and description if empty or changed
    if parsed_feed.feed.get('title') and feed.title != parsed_feed.feed.title:
        feed.title = parsed_feed.feed.title
    if parsed_feed.feed.get('description') and feed.description != parsed_feed.feed.description:
        feed.description = parsed_feed.feed.description
    feed.save()

    for entry in parsed_feed.entries:
        guid = entry.get('id') or entry.get('guid') or entry.get('link')  # Unique identifier
        if not guid:
            continue  # Skip if no unique id

        # Check if item already exists
        if FeedItem.objects.filter(guid=guid).exists():
            continue

        # Parse published date
        published_parsed = entry.get('published_parsed') or entry.get('updated_parsed')
        if published_parsed:
            published = make_aware(datetime(*published_parsed[:6]))
        else:
            published = datetime.now()

        # Create new FeedItem
        FeedItem.objects.create(
            feed=feed,
            guid=guid,
            title=entry.get('title', 'No title'),
            link=entry.get('link', ''),
            summary=entry.get('summary', ''),
            published=published,
        )
