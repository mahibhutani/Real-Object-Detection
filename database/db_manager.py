import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "events.db")


def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            object_id INTEGER,
            timestamp TEXT NOT NULL,
            details TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_event(event_type, object_id, timestamp, details):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO events (event_type, object_id, timestamp, details)
        VALUES (?, ?, ?, ?)
    """, (event_type, object_id, timestamp, details))

    conn.commit()
    conn.close()


def get_events():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, event_type, object_id, timestamp, details
        FROM events
        ORDER BY id DESC
    """)

    events = cursor.fetchall()
    conn.close()

    return events


def clear_events():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM events")
    conn.commit()
    conn.close()