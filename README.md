# AI News Aggregator

A sophisticated news aggregation system that automatically collects, processes, and delivers personalized AI news digests via email. This project demonstrates advanced patterns in data pipeline orchestration, LLM integration, and distributed content processing.

## Overview

**AI News Aggregator** is an intelligent system that:
- **Scrapes content** from multiple AI-focused sources (YouTube channels, RSS feeds)
- **Processes content** using AI to extract key information and generate summaries
- **Curates digests** by ranking articles based on personalized user preferences
- **Delivers digests** as formatted HTML emails to subscribers

The system runs on a scheduled basis, automatically aggregating the latest AI news and delivering a personalized digest directly to your inbox.

## Key Features

- **Multi-source Aggregation**: Scrapes YouTube, RSS feeds (OpenAI, Anthropic, and custom sources)
- **AI-Powered Processing**: Uses Google Gemini API for intelligent summarization and content extraction
- **Personalization Engine**: Ranks content based on configurable user profiles and interests
- **Duplicate Detection**: Prevents sending duplicate articles across digest batches
- **Modular Architecture**: Easy to extend with new scrapers and processors
- **Database Persistence**: PostgreSQL-backed storage for articles, digests, and user data
- **Registry Pattern**: Extensible architecture for adding new content sources

## Architecture

```
Scrapers (YouTube, RSS feeds) 
         ↓
    [Database]
         ↓
Processors (Markdown, Transcripts, Summaries)
         ↓
    [Database]
         ↓
Curator Agent (LLM-based ranking)
         ↓
Email Generator & Sender
         ↓
User Inbox
```

## Detailed Flow
![Project Demo](TreeDiagram.png "Tree Diagram")

## Project Structure

```
ai-news-aggregator/
├── app/
│   ├── agent/                 # LLM agents for processing
│   │   ├── base.py           # Base agent class
│   │   ├── curator_agent.py  # Article ranking and selection
│   │   ├── digest_agent.py   # Summary generation
│   │   └── email_agent.py    # Email content generation
│   ├── config.py             # Configuration (YouTube channels, RSS feeds)
│   ├── database/             # Database layer
│   │   ├── models.py         # SQLAlchemy ORM models
│   │   ├── repository.py     # Data access layer
│   │   ├── connection.py     # Database connection management
│   │   └── create_tables.py  # Schema initialization
│   ├── profiles/             # User configuration
│   │   └── user_profile.py   # User preferences and interests
│   ├── scrapers/             # Content collection
│   │   ├── base.py           # Base scraper for RSS feeds
│   │   ├── anthropic.py      # Anthropic blog scraper
│   │   ├── openai.py         # OpenAI blog scraper
│   │   └── youtube.py        # YouTube channel scraper
│   ├── services/             # Content processing
│   │   ├── base.py           # Base service class
│   │   ├── process_anthropic.py
│   │   ├── process_youtube.py
│   │   ├── process_digest.py
│   │   ├── process_curator.py
│   │   ├── process_email.py
│   │   └── email.py          # Email sending service
│   ├── daily_runner.py       # Main orchestration pipeline
│   ├── runner.py             # Scraper execution registry
│   └── example.env           # Environment template
├── main.py                   # Entry point
├── pyproject.toml           # Project dependencies
└── README.md                # This file
```

## How It Works

### 1. Scraping Phase
- Collects articles from configured YouTube channels and RSS feeds
- Extracts metadata (title, URL, publish date, source)
- Stores raw content in the database for processing

### 2. Processing Phase
- **Markdown Conversion**: Converts HTML articles to readable markdown
- **YouTube Transcripts**: Extracts and processes video transcripts
- **Digest Generation**: Generates summaries using Google Gemini's LLM

### 3. Curation Phase
- Uses the Curator Agent to rank articles by relevance
- Filters based on user profile (interests, expertise level, preferences)
- Selects top N articles for the digest

### 4. Email Delivery
- Formats curated content as HTML email
- Adds personalization
- Tracks which digests have been sent to prevent duplicates
- Sends via Gmail SMTP

### 5. Scheduling
- The system can run on a schedule (daily recommended)
- Or execute manually via command line

## Getting Started

### Prerequisites

- Python 3.12 or higher
- PostgreSQL database
- Google Gemini API key
- Gmail account with app password (for email sending)
- Webshare proxy account (optional, for YouTube transcripts)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-news-aggregator.git
   cd ai-news-aggregator
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   cp app/example.env .env
   ```
   
   Edit `.env` and fill in:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key
   MY_EMAIL=your_gmail@gmail.com
   APP_PASSWORD=your_gmail_app_password
   DATABASE_URL=postgresql://user:password@localhost:5432/ai_news_aggregator
   
   # Optional: Webshare proxy for YouTube transcripts
   WEBSHARE_USERNAME=your_username
   WEBSHARE_PASSWORD=your_password
   ```

4. **Initialize database**
   ```bash
   uv run python -m app.database.create_tables
   ```

5. **Configure sources**
   - Edit `app/config.py` to add/remove YouTube channels
   - Modify `app/profiles/user_profile.py` to customize interests

### Running the Aggregator

**Full pipeline:**
```bash
uv run main.py
```

**With parameters:**
```bash
uv run main.py [hours] [top_n]
# Example: uv run main.py 48 10
# Scrapes last 48 hours, selects top 10 articles
```

**Individual steps:**
```bash
# Scraping only
uv run python -m app.runner

# Processing
uv run python -m app.services.process_anthropic
uv run python -m app.services.process_youtube
uv run python -m app.services.process_digest

# Curation
uv run python -m app.services.process_curator

# Email
uv run python -m app.services.process_email
```

## Configuration

### YouTube Channels
Edit `app/config.py`:
```python
YOUTUBE_CHANNELS = [
    "UCawZsQWqfGSbCI5yjkdVkTA",  # Add channel IDs
]
```

### User Profile
Customize `app/profiles/user_profile.py`:
```python
USER_PROFILE = {
    "name": "Your Name",
    "interests": [
        "Large Language Models",
        "AI agents",
        # Add your interests
    ],
    "preferences": {
        "prefer_practical": True,
        "prefer_technical_depth": True,
    }
}
```

### Database Configuration
The system supports both single `DATABASE_URL` and individual `POSTGRES_*` variables. For local development with docker-compose:

```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ai_news_aggregator
```

## Database Models

The system uses SQLAlchemy ORM with the following main models:
- **Articles**: Raw scraped content
- **Digests**: Processed and ranked articles
- **Sent Digests**: Track what has been sent to prevent duplicates

Refer to `app/database/models.py` for complete schema.

## Extending the System

### Adding a New RSS Feed Source

Create a new scraper in `app/scrapers/`:

```python
from .base import BaseScraper, Article

class MySourceScraper(BaseScraper):
    @property
    def rss_urls(self) -> List[str]:
        return ["https://example.com/feed.xml"]
```

Register it in `app/runner.py`:
```python
SCRAPER_REGISTRY = [
    ("my_source", MySourceScraper(), _save_rss_articles),
]
```

### Adding a Custom Processor

Inherit from `app/services/base.py` and implement the process method:

```python
from app.services.base import BaseService

class MyProcessor(BaseService):
    def process(self) -> dict:
        # Your processing logic
        pass
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.12+ |
| Package Manager | UV |
| Web Framework | None (CLI-based) |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0+ |
| LLM | Google Gemini API |
| Scraping | BeautifulSoup4, feedparser |
| Email | Gmail SMTP |
| Data Validation | Pydantic |

## Performance Considerations

- **Batch Processing**: Articles are processed in batches for efficiency
- **Caching**: Article content is cached to minimize API calls
- **Duplicate Detection**: Prevents redundant email sends
- **Lazy Loading**: Database queries use lazy loading patterns

## Troubleshooting

**Database Connection Issues**
```bash
uv run python -m app.database.create_tables
```

**Email Sending Fails**
- Verify Gmail app password (not regular password)
- Check `MY_EMAIL` and `APP_PASSWORD` environment variables
- Ensure less secure apps are enabled (if applicable)

**Missing Transcripts**
- YouTube Transcript API may rate-limit
- Optional: Use Webshare proxy by setting `WEBSHARE_USERNAME` and `WEBSHARE_PASSWORD`

## Future Enhancements

- [ ] Web dashboard for viewing digests
- [ ] Admin panel for configuration
- [ ] Multiple user profiles
- [ ] Advanced filtering and search
- [ ] Export to RSS/JSON formats
- [ ] API endpoint for digests
- [ ] Measure click events for users which would help to customize user preferences.