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
    """Create tables if they don't exist. Run migrations."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS vocab_attempts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            dutch       TEXT NOT NULL,
            english     TEXT NOT NULL,
            category    TEXT NOT NULL,
            cefr        TEXT NOT NULL DEFAULT '',
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

    # Migration: add cefr column to existing databases
    try:
        conn.execute("ALTER TABLE vocab_attempts ADD COLUMN cefr TEXT NOT NULL DEFAULT ''")
    except Exception:
        pass  # column already exists

    conn.commit()
    conn.close()


# ── Vocab helpers ──────────────────────────────────────────────────────

def record_vocab(dutch, english, category, user_answer, correct, direction, cefr=""):
    conn = get_db()
    conn.execute(
        "INSERT INTO vocab_attempts (dutch, english, category, cefr, user_answer, correct, direction) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (dutch, english, category, cefr, user_answer, int(correct), direction),
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


# ── Dashboard / progress helpers ───────────────────────────────────────

def cefr_progress():
    """Per-CEFR-level: known words (>=50% accuracy), total words attempted."""
    conn = get_db()
    rows = conn.execute("""
        SELECT cefr,
               COUNT(DISTINCT dutch) AS total_seen,
               SUM(CASE WHEN correct THEN 1 ELSE 0 END) AS correct_count,
               COUNT(*) AS attempts
          FROM vocab_attempts
         WHERE cefr IS NOT NULL AND cefr != ''
         GROUP BY cefr
         ORDER BY cefr
    """).fetchall()
    conn.close()
    results = []
    for r in rows:
        d = dict(r)
        # Count distinct words seen, and how many have >= 50% accuracy
        conn2 = get_db()
        word_stats = conn2.execute("""
            SELECT dutch,
                   SUM(correct) AS w_correct,
                   COUNT(*) AS w_total
              FROM vocab_attempts
             WHERE cefr = ?
             GROUP BY dutch
        """, (d["cefr"],)).fetchall()
        conn2.close()
        known = sum(1 for w in word_stats if w["w_correct"] > 0 and (w["w_correct"] * 1.0 / w["w_total"]) >= 0.5)
        d["known"] = known
        d["accuracy"] = round(100 * d["correct_count"] / d["attempts"]) if d["attempts"] else 0
        results.append(d)
    return results


def conjugate_tense_stats():
    """Accuracy per tense."""
    conn = get_db()
    rows = conn.execute("""
        SELECT tense,
               COUNT(*) AS total,
               SUM(correct) AS correct_count,
               ROUND(100.0 * SUM(correct) / COUNT(*), 1) AS pct
          FROM conjugate_attempts
         GROUP BY tense
         ORDER BY pct
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def daily_streak():
    """Return current streak, longest streak, total active days."""
    conn = get_db()
    rows = conn.execute("""
        SELECT DISTINCT date(created_at) AS d
          FROM vocab_attempts
        UNION
        SELECT DISTINCT date(created_at) AS d
          FROM conjugate_attempts
        ORDER BY d DESC
    """).fetchall()
    conn.close()

    if not rows:
        return {"current": 0, "longest": 0, "total_days": 0}

    from datetime import date, timedelta
    today = date.today()
    dates = [date.fromisoformat(r["d"]) for r in rows]

    # Current streak: count consecutive days from today backwards
    current = 0
    check = today
    while check in dates:
        current += 1
        check -= timedelta(days=1)

    # Longest streak
    longest = 1
    streak = 1
    for i in range(1, len(dates)):
        if (dates[i-1] - dates[i]).days == 1:
            streak += 1
            longest = max(longest, streak)
        else:
            streak = 1

        return {
        "current": current,
        "longest": max(longest, current),
        "total_days": len(dates),
    }


# ── LLM explanation cache ──────────────────────────────────────────────

def _ensure_llm_cache_table():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS llm_cache (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            dutch       TEXT NOT NULL,
            expected    TEXT NOT NULL,
            user_answer TEXT NOT NULL,
            acceptable  INTEGER NOT NULL,
            explanation TEXT NOT NULL,
            created_at  TEXT NOT NULL DEFAULT (datetime('now')),
            UNIQUE(dutch, expected, user_answer)
        );
    """)
    conn.commit()
    conn.close()


def llm_cache_lookup(dutch, expected, user_answer):
    """Return cached result or None."""
    _ensure_llm_cache_table()
    conn = get_db()
    row = conn.execute(
        "SELECT acceptable, explanation FROM llm_cache WHERE dutch = ? AND expected = ? AND user_answer = ?",
        (dutch, expected, user_answer),
    ).fetchone()
    conn.close()
    if row:
        return {"acceptable": bool(row["acceptable"]), "explanation": row["explanation"]}
    return None


def llm_cache_store(dutch, expected, user_answer, acceptable, explanation):
    """Store LLM result, skip if dupe."""
    _ensure_llm_cache_table()
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO llm_cache (dutch, expected, user_answer, acceptable, explanation) VALUES (?, ?, ?, ?, ?)",
            (dutch, expected, user_answer, int(acceptable), explanation),
        )
        conn.commit()
    except Exception:
        pass  # ignore duplicates
    conn.close()
