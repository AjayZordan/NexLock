import sqlite3
import json
import time
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "cache.db")
CACHE_EXPIRY_SECONDS = 60 * 60 * 24  # 24 hours


def init_db():
    """Creates the cache table if it doesn't exist yet."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vuln_cache (
            package_name TEXT,
            version TEXT,
            ecosystem TEXT,
            vulnerabilities TEXT,
            checked_at INTEGER,
            PRIMARY KEY (package_name, version, ecosystem)
        )
    """)
    conn.commit()
    conn.close()


def get_cached_result(package_name, version, ecosystem="npm"):
    """
    Returns cached vulnerabilities list if a fresh entry exists, else None.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT vulnerabilities, checked_at FROM vuln_cache
        WHERE package_name = ? AND version = ? AND ecosystem = ?
    """, (package_name, version, ecosystem))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    vulnerabilities_json, checked_at = row
    age = time.time() - checked_at

    if age > CACHE_EXPIRY_SECONDS:
        return None  # cache expired, needs a fresh check

    return json.loads(vulnerabilities_json)


def save_to_cache(package_name, version, vulnerabilities, ecosystem="npm"):
    """Stores a scan result in the cache."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO vuln_cache
        (package_name, version, ecosystem, vulnerabilities, checked_at)
        VALUES (?, ?, ?, ?, ?)
    """, (package_name, version, ecosystem, json.dumps(vulnerabilities), int(time.time())))
    conn.commit()
    conn.close()


# Initialize the DB as soon as this module is imported
init_db()