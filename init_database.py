import sqlite3
from contextlib import closing

import db_info

with closing(sqlite3.connect(db_info.db_name)) as connection:
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS articles("
            "news_id TEXT PRIMARY KEY, "
            "date TEXT, "
            "article TEXT, "
            "init_location TEXT, "
            "processed BOOLEAN)"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS news_crime_types("
            "news_id TEXT, "
            "crime_type TEXT, "
            "FOREIGN KEY(news_id) REFERENCES articles(news_id)) "
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS news_location("
            "news_id TEXT, "
            "location_address TEXT, "
            "coordinate TEXT, "
            "FOREIGN KEY(news_id) REFERENCES articles(news_id)) "
        )
    connection.commit()
