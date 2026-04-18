# Database Management

## Database Configuration

Configure your PostgreSQL database connection using environment variables:

```bash
# Database Connection (defaults provided for local development)
DATABASE_URL=postgresql://user:pass@host:port/db

# Or use individual variables for local development:
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ai_news_aggregator
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

## Setup

### Create Tables

```bash
# Automatically creates all tables if they don't exist
python -m app.database.create_tables
```

Or tables are created automatically on first pipeline run:

```bash
# Tables are initialized when running the pipeline
python main.py
```

## Database Access

The connection module provides:

- `engine` - SQLAlchemy engine for direct query execution
- `SessionLocal` - Session factory for database operations
- `get_session()` - Get a database session instance

## Models

All database models are defined in `models.py` using SQLAlchemy ORM.

## Best Practices

1. **Always check connection** before running migrations
2. **Use individual POSTGRES_* variables** for local development
3. **Keep .env file local** - never commit credentials
4. **Verify database URL** format before connecting

