"""
SQLite models for the Dutch Driller app.
Tracks attempt history per drill type so we can weight questions
toward words/verbs the user struggles with.
"""

import sqlite3
import os
from datetime import datetime, timezone

DB_PATH = os.path.join(os.path.dirname(__file__), "drills.db")


def get_db():
    """Return a connection with row_factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS vocab_attempts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            dutch       TEXT NOT NULL,
            english     TEXT NOT NULL,
            category    TEXT NOT NULL,
            user_answer TEXT NOT NULL,
            correct     INTEGER NOT NULL,  -- 0 or 1
            direction   TEXT NOT NULL,      -- 'nl_en' or 'en_nl'
            created_at  TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS conjugate_attempts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            infinitive  TEXT NOT NULL,
            tense       TEXT NOT NULL,
            pronoun     TEXT NOT NULL,
            user_answer TEXT NOT NULL,
            correct     INTEGER NOT NULL,
            created_at  TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_vocab_word ON vocab_attempts(dutch, direction);
        CREATE INDEX IF NOT EXISTS idx_vocab_correct ON vocab_attempts(dutch, correct);
        CREATE INDEX IF NOT EXISTS idx_verb_attempt ON conjugate_attempts(infinitive, tense, pronoun);
    """)
    conn.commit()
    conn.close()


# ── Vocab helpers ──────────────────────────────────────────────────────

def record_vocab(dutch, english, category, user_answer, correct, direction):
    conn = get_db()
    conn.execute(
        "INSERT INTO vocab_attempts (dutch, english, category, user_answer, correct, direction) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (dutch, english, category, user_answer, int(correct), direction),
    )
    conn.commit()
    conn.close()


def vocab_stats(direction="nl_en"):
    """Return per-word stats: total attempts, correct count, accuracy %."""
    conn = get_db()
    rows = conn.execute("""
        SELECT dutch, english, category,
               COUNT(*) AS total,
               SUM(correct) AS correct_count,
               ROUND(100.0 * SUM(correct) / COUNT(*), 1) AS pct
          FROM vocab_attempts
         WHERE direction = ?
         GROUP BY dutch, english, category
         ORDER BY pct ASC, total DESC
    """, (direction,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def vocab_overall():
    """Total correct vs total attempts."""
    conn = get_db()
    row = conn.execute("""
        SELECT COUNT(*) AS total,
               SUM(correct) AS correct_count
          FROM vocab_attempts
    """).fetchone()
    conn.close()
    return dict(row) if row else {"total": 0, "correct_count": 0}


# ── Conjugation helpers ─────────────────────────────────────────────────

def record_conjugate(infinitive, tense, pronoun, user_answer, correct):
    conn = get_db()
    conn.execute(
        "INSERT INTO conjugate_attempts (infinitive, tense, pronoun, user_answer, correct) "
        "VALUES (?, ?, ?, ?, ?)",
        (infinitive, tense, pronoun, user_answer, int(correct)),
    )
    conn.commit()
    conn.close()


def conjugate_stats():
    """Per-verb+tense+pronoun stats."""
    conn = get_db()
    rows = conn.execute("""
        SELECT infinitive, tense, pronoun,
               COUNT(*) AS total,
               SUM(correct) AS correct_count,
               ROUND(100.0 * SUM(correct) / COUNT(*), 1) AS pct
          FROM conjugate_attempts
         GROUP BY infinitive, tense, pronoun
         ORDER BY pct ASC, total DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def conjugate_overall():
    conn = get_db()
    row = conn.execute("""
        SELECT COUNT(*) AS total,
               SUM(correct) AS correct_count
          FROM conjugate_attempts
    """).fetchone()
    conn.close()
    return dict(row) if row else {"total": 0, "correct_count": 0}
