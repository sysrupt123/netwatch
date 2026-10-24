import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("traffic.db")


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # rows behave like dictionaries
    return conn


def init_db():
    conn = connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            domain TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def insert_query(domain, category):
    conn = connect()
    # the ? placeholders are a parameterized query (see note below)
    conn.execute(
        "INSERT INTO queries (ts, domain, category) "
        "VALUES (datetime('now', 'localtime'), ?, ?)",
        (domain, category),
    )
    conn.commit()
    conn.close()


def recent(limit=20):
    conn = connect()
    rows = conn.execute(
        "SELECT ts, domain, category FROM queries ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def category_counts():
    conn = connect()
    rows = conn.execute(
        "SELECT category, COUNT(*) AS n FROM queries "
        "GROUP BY category ORDER BY n DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def top_domains(limit=10):
    conn = connect()
    rows = conn.execute(
        "SELECT domain, COUNT(*) AS n FROM queries "
        "GROUP BY domain ORDER BY n DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def totals():
    conn = connect()
    row = conn.execute(
        "SELECT COUNT(*) AS total, COUNT(DISTINCT domain) AS uniq FROM queries"
    ).fetchone()
    last = conn.execute(
        "SELECT COUNT(*) AS n FROM queries "
        "WHERE ts >= datetime('now', 'localtime', '-1 minutes')"
    ).fetchone()
    conn.close()
    return {"total": row["total"], "unique": row["uniq"], "last_minute": last["n"]}


def per_minute(minutes=30):
    conn = connect()
    rows = conn.execute(
        "SELECT strftime('%H:%M', ts) AS minute, COUNT(*) AS n FROM queries "
        "WHERE ts >= datetime('now', 'localtime', ?) GROUP BY minute",
        (f"-{minutes} minutes",),
    ).fetchall()
    conn.close()
    return {r["minute"]: r["n"] for r in rows}
