tables = (
    """
    CREATE TABLE IF NOT EXISTS short_url (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            original_url TEXT NOT NULL,
            shortUrl TEXT NOT NULL
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS short_url_metadata (
            shortUrl TEXT NOT NULL,
            total_hits INTEGER,
        )
    """,
)
