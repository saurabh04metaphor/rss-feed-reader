# FeedFlow

A Django-based RSS feed reader application that allows users to manage and read their favorite RSS feeds in one place.

## Features

- User authentication (signup/login)
- Subscribe to RSS feeds by adding feed URLs
- Automatically fetches and updates feed content
- View all articles from subscribed feeds in chronological order
- Filter articles by specific feed
- Mark articles as read/unread
- Unsubscribe from feeds
- Responsive web interface

## Technology Stack

- Python 3.12
- Django
- SQLite3
- feedparser (for RSS parsing)
- HTML/CSS for frontend

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rss_reader.git
cd rss_reader
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run database migrations:
```bash
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

5. Visit `http://localhost:8000` in your web browser

## Feed Updates

The application includes a management command to update all feeds:

```bash
python manage.py update_feeds
```

For automated updates, you can set up a scheduled task (cron job on Linux/Mac or Task Scheduler on Windows) to run this command periodically.

On Windows, the included `update_feeds.bat` can be used with Task Scheduler.

## Project Structure

- `feed_reader/` - Main application directory
  - `models.py` - Database models for feeds and articles
  - `views.py` - View functions handling user requests
  - `utils.py` - Utility functions for feed parsing
  - `forms.py` - Form definitions
  - `templates/` - HTML templates
  - `management/commands/` - Custom management commands

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
