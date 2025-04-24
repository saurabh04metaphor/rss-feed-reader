import feedparser
from datetime import datetime
from django.utils.timezone import make_aware
import logging
from .models import Feed, FeedItem

logger = logging.getLogger(__name__)

def update_feed_items(feed: Feed):
    logger.info(f"Updating feed: {feed.url}")
    parsed_feed = feedparser.parse(feed.url)
    logger.debug(f"Parsed feed: {parsed_feed.feed}")

    if parsed_feed.feed.get('title') and feed.title != parsed_feed.feed.title:
        feed.title = parsed_feed.feed.title
    if parsed_feed.feed.get('description') and feed.description != parsed_feed.feed.description:
        feed.description = parsed_feed.feed.description
    feed.save()

    for entry in parsed_feed.entries:
        guid = entry.get('id') or entry.get('guid') or entry.get('link')
        if not guid:
            logger.warning(f"Skipping entry without GUID: {entry}")
            continue

        if FeedItem.objects.filter(feed=feed, guid=guid).exists():
            logger.info(f"Skipping existing item with GUID: {guid} for feed: {feed.id}")
            continue

        published_parsed = entry.get('published_parsed') or entry.get('updated_parsed')
        if published_parsed:
            published = make_aware(datetime(*published_parsed[:6]))
        else:
            published = datetime.now()

        FeedItem.objects.create(
            feed=feed,
            guid=guid,
            title=entry.get('title', 'No title'),
            link=entry.get('link', ''),
            summary=entry.get('summary', ''),
            published=published,
        )
        logger.info(f"Created FeedItem with GUID: {guid}")
