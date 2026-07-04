"""
SQLite models for the Dutch Driller app.
Tracks attempt history per drill type + spaced repetition state.

Column naming convention (language-agnostic):
  word        = the target-language word/phrase
  translation = the English translation
  direction   = 'forward' (word→translation) or 'reverse' (translation→word)
  lang        = language code ('nl', 'es', etc.)
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


# ── Schema + migration ──────────────────────────────────────────────────

def _has_column(conn, table, column):
    """Check if a column exists in a table."""
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(r[1] == column for r in rows)


def _migrate_schema(conn):
    """One-time migration: rename columns, add lang, fix direction values."""

    # ── vocab_attempts ──────────────────────────────────────────────
    if _has_column(conn, "vocab_attempts", "dutch") and not _has_column(conn, "vocab_attempts", "word"):
        conn.execute("ALTER TABLE vocab_attempts RENAME COLUMN dutch TO word")
    if _has_column(conn, "vocab_attempts", "english") and not _has_column(conn, "vocab_attempts", "translation"):
        conn.execute("ALTER TABLE vocab_attempts RENAME COLUMN english TO translation")
    if not _has_column(conn, "vocab_attempts", "lang"):
        conn.execute("ALTER TABLE vocab_attempts ADD COLUMN lang TEXT NOT NULL DEFAULT 'nl'")
    conn.execute("UPDATE vocab_attempts SET direction='forward' WHERE direction='nl_en'")
    conn.execute("UPDATE vocab_attempts SET direction='reverse' WHERE direction='en_nl'")

    # ── vocab_words ─────────────────────────────────────────────────
    if _has_column(conn, "vocab_words", "dutch") and not _has_column(conn, "vocab_words", "word"):
        conn.execute("ALTER TABLE vocab_words RENAME COLUMN dutch TO word")
    if _has_column(conn, "vocab_words", "english") and not _has_column(conn, "vocab_words", "translation"):
        conn.execute("ALTER TABLE vocab_words RENAME COLUMN english TO translation")
    if not _has_column(conn, "vocab_words", "lang"):
        conn.execute("ALTER TABLE vocab_words ADD COLUMN lang TEXT NOT NULL DEFAULT 'nl'")

    # ── phrases ─────────────────────────────────────────────────────
    if _has_column(conn, "phrases", "dutch") and not _has_column(conn, "phrases", "word"):
        conn.execute("ALTER TABLE phrases RENAME COLUMN dutch TO word")
    if _has_column(conn, "phrases", "english") and not _has_column(conn, "phrases", "translation"):
        conn.execute("ALTER TABLE phrases RENAME COLUMN english TO translation")
    if not _has_column(conn, "phrases", "lang"):
        conn.execute("ALTER TABLE phrases ADD COLUMN lang TEXT NOT NULL DEFAULT 'nl'")

    # ── verbs_ref ───────────────────────────────────────────────────
    if _has_column(conn, "verbs_ref", "english") and not _has_column(conn, "verbs_ref", "translation"):
        conn.execute("ALTER TABLE verbs_ref RENAME COLUMN english TO translation")
    if not _has_column(conn, "verbs_ref", "lang"):
        conn.execute("ALTER TABLE verbs_ref ADD COLUMN lang TEXT NOT NULL DEFAULT 'nl'")

    # ── sentences_ref ───────────────────────────────────────────────
    if not _has_column(conn, "sentences_ref", "lang"):
        conn.execute("ALTER TABLE sentences_ref ADD COLUMN lang TEXT NOT NULL DEFAULT 'nl'")

    # ── vocab_srs: rebuild with lang in PK ──────────────────────────
    if not _has_column(conn, "vocab_srs", "lang"):
        # Rebuild table with new schema
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS vocab_srs_new (
                word        TEXT NOT NULL,
                direction   TEXT NOT NULL,
                lang        TEXT NOT NULL DEFAULT 'nl',
                ef          REAL NOT NULL DEFAULT 2.5,
                interval    INTEGER NOT NULL DEFAULT 1,
                reps        INTEGER NOT NULL DEFAULT 0,
                next_review TEXT NOT NULL DEFAULT (date('now')),
                last_review TEXT,
                PRIMARY KEY (word, direction, lang)
            );
        """)
        has_old = _has_column(conn, "vocab_srs", "word") or _has_column(conn, "vocab_srs", "dutch")
        if has_old:
            src_col = "word" if _has_column(conn, "vocab_srs", "word") else "dutch"
            conn.execute(f"""
                INSERT OR IGNORE INTO vocab_srs_new (word, direction, lang, ef, interval, reps, next_review, last_review)
                SELECT {src_col}, direction, 'nl', ef, interval, reps, next_review, last_review FROM vocab_srs
            """)
        conn.execute("DROP TABLE IF EXISTS vocab_srs")
        conn.execute("ALTER TABLE vocab_srs_new RENAME TO vocab_srs")
        conn.execute("UPDATE vocab_srs SET direction='forward' WHERE direction='nl_en'")
        conn.execute("UPDATE vocab_srs SET direction='reverse' WHERE direction='en_nl'")

    # ── conjugate_srs: add lang to PK ───────────────────────────────
    if not _has_column(conn, "conjugate_srs", "lang"):
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS conjugate_srs_new (
                infinitive  TEXT NOT NULL,
                tense       TEXT NOT NULL,
                pronoun     TEXT NOT NULL,
                lang        TEXT NOT NULL DEFAULT 'nl',
                ef          REAL NOT NULL DEFAULT 2.5,
                interval    INTEGER NOT NULL DEFAULT 1,
                reps        INTEGER NOT NULL DEFAULT 0,
                next_review TEXT NOT NULL DEFAULT (date('now')),
                last_review TEXT,
                PRIMARY KEY (infinitive, tense, pronoun, lang)
            );
        """)
        if _has_column(conn, "conjugate_srs", "infinitive"):
            conn.execute("""
                INSERT OR IGNORE INTO conjugate_srs_new (infinitive, tense, pronoun, lang, ef, interval, reps, next_review, last_review)
                SELECT infinitive, tense, pronoun, 'nl', ef, interval, reps, next_review, last_review FROM conjugate_srs
            """)
        conn.execute("DROP TABLE IF EXISTS conjugate_srs")
        conn.execute("ALTER TABLE conjugate_srs_new RENAME TO conjugate_srs")

    # ── conjugate_attempts: add lang ────────────────────────────────
    if not _has_column(conn, "conjugate_attempts", "lang"):
        conn.execute("ALTER TABLE conjugate_attempts ADD COLUMN lang TEXT NOT NULL DEFAULT 'nl'")


def init_db():
    """Create tables if they don't exist. Run migrations."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS vocab_attempts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            word        TEXT NOT NULL,
            translation TEXT NOT NULL,
            category    TEXT NOT NULL,
            cefr        TEXT NOT NULL DEFAULT '',
            user_answer TEXT NOT NULL,
            correct     INTEGER NOT NULL,
            direction   TEXT NOT NULL,
            lang        TEXT NOT NULL DEFAULT 'nl',
            created_at  TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS conjugate_attempts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            infinitive  TEXT NOT NULL,
            tense       TEXT NOT NULL,
            pronoun     TEXT NOT NULL,
            user_answer TEXT NOT NULL,
            correct     INTEGER NOT NULL,
            lang        TEXT NOT NULL DEFAULT 'nl',
            created_at  TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_vocab_word ON vocab_attempts(word, direction, lang);
        CREATE INDEX IF NOT EXISTS idx_vocab_correct ON vocab_attempts(word, correct);
        CREATE INDEX IF NOT EXISTS idx_verb_attempt ON conjugate_attempts(infinitive, tense, pronoun);

        CREATE TABLE IF NOT EXISTS vocab_srs (
            word        TEXT NOT NULL,
            direction   TEXT NOT NULL,
            lang        TEXT NOT NULL DEFAULT 'nl',
            ef          REAL NOT NULL DEFAULT 2.5,
            interval    INTEGER NOT NULL DEFAULT 1,
            reps        INTEGER NOT NULL DEFAULT 0,
            next_review TEXT NOT NULL DEFAULT (date('now')),
            last_review TEXT,
            PRIMARY KEY (word, direction, lang)
        );

        CREATE TABLE IF NOT EXISTS conjugate_srs (
            infinitive  TEXT NOT NULL,
            tense       TEXT NOT NULL,
            pronoun     TEXT NOT NULL,
            lang        TEXT NOT NULL DEFAULT 'nl',
            ef          REAL NOT NULL DEFAULT 2.5,
            interval    INTEGER NOT NULL DEFAULT 1,
            reps        INTEGER NOT NULL DEFAULT 0,
            next_review TEXT NOT NULL DEFAULT (date('now')),
            last_review TEXT,
            PRIMARY KEY (infinitive, tense, pronoun, lang)
        );
        CREATE INDEX IF NOT EXISTS idx_conjugate_srs_tense ON conjugate_srs(tense, next_review);

        CREATE TABLE IF NOT EXISTS vocab_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            translation TEXT NOT NULL,
            category TEXT NOT NULL,
            lang TEXT NOT NULL DEFAULT 'nl',
            cefr TEXT NOT NULL DEFAULT '',
            example TEXT NOT NULL DEFAULT '',
            audio_url TEXT NOT NULL DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS phrases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            translation TEXT NOT NULL,
            scenario TEXT NOT NULL,
            lang TEXT NOT NULL DEFAULT 'nl',
            cefr TEXT NOT NULL DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS sentences_ref (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            correct_order TEXT NOT NULL,
            english TEXT NOT NULL,
            lang TEXT NOT NULL DEFAULT 'nl',
            cefr TEXT NOT NULL DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS verbs_ref (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            infinitive TEXT NOT NULL UNIQUE,
            translation TEXT NOT NULL,
            type TEXT NOT NULL,
            stem TEXT NOT NULL DEFAULT '',
            lang TEXT NOT NULL DEFAULT 'nl',
            cefr TEXT NOT NULL DEFAULT '',
            example TEXT NOT NULL DEFAULT '',
            irregular TEXT NOT NULL DEFAULT '{}'
        );
    """)

    # Run migrations for existing databases
    _migrate_schema(conn)

    conn.commit()
    conn.close()


# ── Vocab helpers ──────────────────────────────────────────────────────

def record_vocab(word, translation, category, user_answer, correct, direction, lang="nl", cefr=""):
    conn = get_db()
    conn.execute(
        "INSERT INTO vocab_attempts (word, translation, category, cefr, user_answer, correct, direction, lang) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (word, translation, category, cefr, user_answer, int(correct), direction, lang),
    )
    conn.commit()
    conn.close()


def vocab_stats(direction="forward"):
    """Return per-word stats: total attempts, correct count, accuracy %."""
    conn = get_db()
    rows = conn.execute("""
        SELECT word, translation, category,
               COUNT(*) AS total,
               SUM(correct) AS correct_count,
               ROUND(100.0 * SUM(correct) / COUNT(*), 1) AS pct
          FROM vocab_attempts
         WHERE direction = ?
         GROUP BY word, translation, category
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

def record_conjugate(infinitive, tense, pronoun, user_answer, correct, lang="nl"):
    conn = get_db()
    conn.execute(
        "INSERT INTO conjugate_attempts (infinitive, tense, pronoun, user_answer, correct, lang) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (infinitive, tense, pronoun, user_answer, int(correct), lang),
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
               COUNT(DISTINCT word) AS total_seen,
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
        conn2 = get_db()
        word_stats = conn2.execute("""
            SELECT word,
                   SUM(correct) AS w_correct,
                   COUNT(*) AS w_total
              FROM vocab_attempts
             WHERE cefr = ?
             GROUP BY word
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

    current = 0
    check = today
    while check in dates:
        current += 1
        check -= timedelta(days=1)

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


# ── Reference data access ──────────────────────────────────────────────

def _ensure_ref_tables():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS vocab_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            translation TEXT NOT NULL,
            category TEXT NOT NULL,
            lang TEXT NOT NULL DEFAULT 'nl',
            cefr TEXT NOT NULL DEFAULT '',
            example TEXT NOT NULL DEFAULT '',
            audio_url TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS phrases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            translation TEXT NOT NULL,
            scenario TEXT NOT NULL,
            lang TEXT NOT NULL DEFAULT 'nl',
            cefr TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS sentences_ref (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            correct_order TEXT NOT NULL,
            english TEXT NOT NULL,
            lang TEXT NOT NULL DEFAULT 'nl',
            cefr TEXT NOT NULL DEFAULT ''
        );
    """)
    conn.commit()
    conn.close()


def get_vocab_words(category=None, lang="nl"):
    conn = get_db(); _ensure_ref_tables()
    if category:
        rows = conn.execute(
            "SELECT id, word, translation, category, lang, cefr, example, audio_url FROM vocab_words WHERE category=? AND lang=?",
            (category, lang),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, word, translation, category, lang, cefr, example, audio_url FROM vocab_words WHERE lang=?",
            (lang,),
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_vocab_categories(lang="nl"):
    conn = get_db()
    rows = conn.execute(
        "SELECT DISTINCT category FROM vocab_words WHERE lang=? ORDER BY category",
        (lang,),
    ).fetchall()
    conn.close()
    return [r["category"] for r in rows]


def get_phrases(scenario=None, lang="nl"):
    conn = get_db(); _ensure_ref_tables()
    if scenario:
        rows = conn.execute(
            "SELECT id, word, translation, scenario, lang, cefr FROM phrases WHERE scenario=? AND lang=?",
            (scenario, lang),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, word, translation, scenario, lang, cefr FROM phrases WHERE lang=?",
            (lang,),
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_phrase_scenarios(lang="nl"):
    conn = get_db()
    rows = conn.execute(
        "SELECT DISTINCT scenario FROM phrases WHERE lang=? ORDER BY scenario",
        (lang,),
    ).fetchall()
    conn.close()
    return [r["scenario"] for r in rows]


def get_sentences(level=None, lang="nl"):
    conn = get_db(); _ensure_ref_tables()
    if level:
        rows = conn.execute(
            "SELECT id, correct_order, english, lang, cefr FROM sentences_ref WHERE cefr=? AND lang=?",
            (level, lang),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, correct_order, english, lang, cefr FROM sentences_ref WHERE lang=?",
            (lang,),
        ).fetchall()
    conn.close()
    import json
    return [{**dict(r), "correct_order": json.loads(r["correct_order"])} for r in rows]


def get_sentence_levels(lang="nl"):
    conn = get_db()
    rows = conn.execute(
        "SELECT DISTINCT cefr FROM sentences_ref WHERE lang=? ORDER BY cefr",
        (lang,),
    ).fetchall()
    conn.close()
    return [r["cefr"] for r in rows]


# ── Content insert helpers ─────────────────────────────────────────────

def insert_vocab(word, translation, category, cefr, example, lang="nl"):
    conn = get_db(); _ensure_ref_tables()
    try:
        conn.execute(
            "INSERT INTO vocab_words (word, translation, category, lang, cefr, example) VALUES (?,?,?,?,?,?)",
            (word, translation, category, lang, cefr, example),
        )
        conn.commit()
    except Exception:
        pass
    conn.close()


def insert_verb(infinitive, translation, vtype, stem, cefr, example, irregular, lang="nl"):
    conn = get_db(); _ensure_verbs_table()
    import json
    try:
        conn.execute(
            "INSERT INTO verbs_ref (infinitive, translation, type, stem, lang, cefr, example, irregular) VALUES (?,?,?,?,?,?,?,?)",
            (infinitive, translation, vtype, stem, lang, cefr, example, json.dumps(irregular or {})),
        )
        conn.commit()
    except Exception:
        pass
    conn.close()


def insert_phrase(word, translation, scenario, cefr, lang="nl"):
    conn = get_db(); _ensure_ref_tables()
    try:
        conn.execute(
            "INSERT INTO phrases (word, translation, scenario, lang, cefr) VALUES (?,?,?,?,?)",
            (word, translation, scenario, lang, cefr),
        )
        conn.commit()
    except Exception:
        pass
    conn.close()


def insert_sentence(correct_order, english, cefr, lang="nl"):
    conn = get_db(); _ensure_ref_tables()
    import json
    try:
        conn.execute(
            "INSERT INTO sentences_ref (correct_order, english, lang, cefr) VALUES (?,?,?,?)",
            (json.dumps(correct_order), english, lang, cefr),
        )
        conn.commit()
    except Exception:
        pass
    conn.close()


def get_table_counts():
    conn = get_db()
    return {
        "vocab": conn.execute("SELECT COUNT(*) FROM vocab_words").fetchone()[0],
        "verbs": conn.execute("SELECT COUNT(*) FROM verbs_ref").fetchone()[0],
        "phrases": conn.execute("SELECT COUNT(*) FROM phrases").fetchone()[0],
        "sentences": conn.execute("SELECT COUNT(*) FROM sentences_ref").fetchone()[0],
    }


# ── Verb reference data ────────────────────────────────────────────────

def _ensure_verbs_table():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS verbs_ref (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            infinitive TEXT NOT NULL UNIQUE,
            translation TEXT NOT NULL,
            type       TEXT NOT NULL,
            stem       TEXT NOT NULL DEFAULT '',
            lang       TEXT NOT NULL DEFAULT 'nl',
            cefr       TEXT NOT NULL DEFAULT '',
            example    TEXT NOT NULL DEFAULT '',
            irregular  TEXT NOT NULL DEFAULT '{}'
        );
    """)
    conn.commit()
    conn.close()


def get_verbs(lang="nl"):
    conn = get_db()
    _ensure_verbs_table()
    import json
    rows = conn.execute(
        "SELECT id, infinitive, translation, type, stem, lang, cefr, example, irregular FROM verbs_ref WHERE lang=?",
        (lang,),
    ).fetchall()
    conn.close()
    return [{**dict(r), "irregular": json.loads(r["irregular"])} for r in rows]


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
    _ensure_llm_cache_table()
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO llm_cache (dutch, expected, user_answer, acceptable, explanation) VALUES (?, ?, ?, ?, ?)",
            (dutch, expected, user_answer, int(acceptable), explanation),
        )
        conn.commit()
    except Exception:
        pass
    conn.close()


# ── Spaced Repetition (SM-2 Lite) ───────────────────────────────────────

from srs import update as _srs_update


def _upsert_vocab_srs(word, direction, lang, correct):
    """Update or create an SRS row for one vocab/phrase item after an answer."""
    conn = get_db()
    row = conn.execute(
        "SELECT ef, interval, reps FROM vocab_srs WHERE word = ? AND direction = ? AND lang = ?",
        (word, direction, lang),
    ).fetchone()

    if row:
        ef, interval, reps = row["ef"], row["interval"], row["reps"]
    else:
        ef, interval, reps = 2.5, 1, 0

    new_ef, new_interval, new_reps, next_review = _srs_update(ef, interval, reps, correct)

    conn.execute("""
        INSERT INTO vocab_srs (word, direction, lang, ef, interval, reps, next_review, last_review)
        VALUES (?, ?, ?, ?, ?, ?, ?, date('now'))
        ON CONFLICT(word, direction, lang) DO UPDATE SET
            ef = excluded.ef, interval = excluded.interval, reps = excluded.reps,
            next_review = excluded.next_review, last_review = excluded.last_review
    """, (word, direction, lang, new_ef, new_interval, new_reps, next_review))
    conn.commit()
    conn.close()


def _upsert_conjugate_srs(infinitive, tense, pronoun, lang, correct):
    """Update or create an SRS row for one conjugation item after an answer."""
    conn = get_db()
    row = conn.execute(
        "SELECT ef, interval, reps FROM conjugate_srs WHERE infinitive = ? AND tense = ? AND pronoun = ? AND lang = ?",
        (infinitive, tense, pronoun, lang),
    ).fetchone()

    if row:
        ef, interval, reps = row["ef"], row["interval"], row["reps"]
    else:
        ef, interval, reps = 2.5, 1, 0

    new_ef, new_interval, new_reps, next_review = _srs_update(ef, interval, reps, correct)

    conn.execute("""
        INSERT INTO conjugate_srs (infinitive, tense, pronoun, lang, ef, interval, reps, next_review, last_review)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, date('now'))
        ON CONFLICT(infinitive, tense, pronoun, lang) DO UPDATE SET
            ef = excluded.ef, interval = excluded.interval, reps = excluded.reps,
            next_review = excluded.next_review, last_review = excluded.last_review
    """, (infinitive, tense, pronoun, lang, new_ef, new_interval, new_reps, next_review))
    conn.commit()
    conn.close()


def get_due_vocab(direction, lang, category=None, limit=10):
    """
    Return vocab items prioritized by SRS due-ness.
    Due items (next_review <= today or never reviewed) come first,
    followed by not-yet-due items sorted by soonest review.
    """
    conn = get_db()
    if category:
        rows = conn.execute("""
            SELECT vw.word, vw.translation, vw.category, vw.cefr, vw.example, vw.lang
            FROM vocab_words vw
            LEFT JOIN vocab_srs vs ON vw.word = vs.word AND vs.direction = ? AND vs.lang = ?
            WHERE vw.lang = ? AND vw.category = ?
            ORDER BY
                CASE WHEN vs.next_review IS NULL OR vs.next_review <= date('now') THEN 0 ELSE 1 END,
                vs.next_review ASC
            LIMIT ?
        """, (direction, lang, lang, category, limit)).fetchall()
    else:
        rows = conn.execute("""
            SELECT vw.word, vw.translation, vw.category, vw.cefr, vw.example, vw.lang
            FROM vocab_words vw
            LEFT JOIN vocab_srs vs ON vw.word = vs.word AND vs.direction = ? AND vs.lang = ?
            WHERE vw.lang = ?
            ORDER BY
                CASE WHEN vs.next_review IS NULL OR vs.next_review <= date('now') THEN 0 ELSE 1 END,
                vs.next_review ASC
            LIMIT ?
        """, (direction, lang, lang, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_due_phrases(direction, lang, scenario=None, limit=10):
    """Return phrase items prioritized by SRS due-ness."""
    conn = get_db()
    if scenario:
        rows = conn.execute("""
            SELECT p.word, p.translation, p.scenario, p.cefr, p.lang
            FROM phrases p
            LEFT JOIN vocab_srs vs ON p.word = vs.word AND vs.direction = ? AND vs.lang = ?
            WHERE p.lang = ? AND p.scenario = ?
            ORDER BY
                CASE WHEN vs.next_review IS NULL OR vs.next_review <= date('now') THEN 0 ELSE 1 END,
                vs.next_review ASC
            LIMIT ?
        """, (direction, lang, lang, scenario, limit)).fetchall()
    else:
        rows = conn.execute("""
            SELECT p.word, p.translation, p.scenario, p.cefr, p.lang
            FROM phrases p
            LEFT JOIN vocab_srs vs ON p.word = vs.word AND vs.direction = ? AND vs.lang = ?
            WHERE p.lang = ?
            ORDER BY
                CASE WHEN vs.next_review IS NULL OR vs.next_review <= date('now') THEN 0 ELSE 1 END,
                vs.next_review ASC
            LIMIT ?
        """, (direction, lang, lang, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_due_conjugations(tense, lang, pronouns, limit=10):
    """
    Return verb+pronoun combos prioritized by SRS due-ness.
    Due items come first; remaining slots filled with random unseen combos.
    pronouns should be a dict like {"ik":"I", ...} from the language engine.
    """
    import random

    conn = get_db()
    due = conn.execute("""
        SELECT infinitive, pronoun FROM conjugate_srs
        WHERE tense = ? AND lang = ? AND next_review <= date('now')
        ORDER BY next_review ASC
        LIMIT ?
    """, (tense, lang, limit)).fetchall()
    conn.close()

    verbs = get_verbs(lang)
    pronoun_keys = list(pronouns.keys())

    result = []
    seen = set()

    for row in due:
        key = (row["infinitive"], row["pronoun"])
        if key not in seen:
            verb = next((v for v in verbs if v["infinitive"] == row["infinitive"]), None)
            if verb:
                result.append({**verb, "pronoun": row["pronoun"]})
                seen.add(key)

    if len(result) < limit:
        combos = [(v, p) for v in verbs for p in pronoun_keys]
        random.shuffle(combos)
        for verb, pronoun in combos:
            key = (verb["infinitive"], pronoun)
            if key not in seen:
                result.append({**verb, "pronoun": pronoun})
                seen.add(key)
                if len(result) >= limit:
                    break

    return result[:limit]


# ── SRS Stats ───────────────────────────────────────────────────────────

def srs_vocab_stats(lang="nl"):
    """Return SRS overview stats for vocabulary/phrases."""
    conn = get_db()

    # Queue overview
    queue = conn.execute("""
        SELECT
            COUNT(DISTINCT word) AS total_in_srs,
            SUM(CASE WHEN next_review <= date('now') THEN 1 ELSE 0 END) AS due_now,
            SUM(CASE WHEN next_review <= date('now', '+7 days') THEN 1 ELSE 0 END) AS due_week
        FROM vocab_srs
        WHERE lang = ?
          AND direction = 'forward'
    """, (lang,)).fetchone()

    # Mastery tiers
    mastery = conn.execute("""
        SELECT
            SUM(CASE WHEN reps = 0 THEN 1 ELSE 0 END) AS new_items,
            SUM(CASE WHEN reps BETWEEN 1 AND 2 THEN 1 ELSE 0 END) AS learning,
            SUM(CASE WHEN reps >= 3 THEN 1 ELSE 0 END) AS mature
        FROM vocab_srs
        WHERE lang = ?
          AND direction = 'forward'
    """, (lang,)).fetchone()

    # Interval distribution
    intervals = conn.execute("""
        SELECT
            SUM(CASE WHEN interval = 1 THEN 1 ELSE 0 END) AS i_1d,
            SUM(CASE WHEN interval BETWEEN 2 AND 6 THEN 1 ELSE 0 END) AS i_2_6d,
            SUM(CASE WHEN interval BETWEEN 7 AND 14 THEN 1 ELSE 0 END) AS i_7_14d,
            SUM(CASE WHEN interval BETWEEN 15 AND 30 THEN 1 ELSE 0 END) AS i_15_30d,
            SUM(CASE WHEN interval > 30 THEN 1 ELSE 0 END) AS i_30plus
        FROM vocab_srs
        WHERE lang = ?
          AND direction = 'forward'
    """, (lang,)).fetchone()

    # Average EF
    avg_ef = conn.execute("""
        SELECT ROUND(AVG(ef), 2) AS avg_ef,
               ROUND(AVG(CASE WHEN reps >= 2 THEN ef END), 2) AS avg_ef_mature
        FROM vocab_srs WHERE lang = ? AND direction = 'forward'
    """, (lang,)).fetchone()

    # Per-category breakdown (join vocab_words for category)
    by_category = conn.execute("""
        SELECT vw.category,
               COUNT(*) AS total,
               SUM(CASE WHEN vs.next_review <= date('now') THEN 1 ELSE 0 END) AS due_now,
               ROUND(AVG(vs.ef), 2) AS avg_ef,
               ROUND(AVG(vs.interval), 1) AS avg_interval
        FROM vocab_srs vs
        JOIN vocab_words vw ON vs.word = vw.word AND vs.lang = vw.lang
        WHERE vs.lang = ?
          AND vs.direction = 'forward'
        GROUP BY vw.category
        ORDER BY due_now DESC, avg_ef ASC
    """, (lang,)).fetchall()

    # Reviews in last 7 days
    recent = conn.execute("""
        SELECT COUNT(*) AS reviews_7d
        FROM vocab_attempts
        WHERE lang = ? AND created_at >= datetime('now', '-7 days')
    """, (lang,)).fetchone()

    # Items never reviewed yet
    unseen = conn.execute("""
        SELECT COUNT(*) AS unseen
        FROM vocab_words vw
        WHERE vw.lang = ?
          AND NOT EXISTS (SELECT 1 FROM vocab_srs vs WHERE vs.word = vw.word AND vs.lang = vw.lang)
    """, (lang,)).fetchone()

    conn.close()

    return {
        "queue": dict(queue) if queue else {},
        "mastery": dict(mastery) if mastery else {},
        "intervals": dict(intervals) if intervals else {},
        "avg_ef": dict(avg_ef) if avg_ef else {},
        "by_category": [dict(r) for r in by_category],
        "recent": dict(recent) if recent else {},
        "unseen": dict(unseen) if unseen else {},
    }


def srs_conjugate_stats(lang="nl"):
    """Return SRS overview stats for conjugations."""
    conn = get_db()

    # Queue overview
    queue = conn.execute("""
        SELECT
            COUNT(*) AS total_in_srs,
            SUM(CASE WHEN next_review <= date('now') THEN 1 ELSE 0 END) AS due_now,
            SUM(CASE WHEN next_review <= date('now', '+7 days') THEN 1 ELSE 0 END) AS due_week
        FROM conjugate_srs
        WHERE lang = ?
    """, (lang,)).fetchone()

    # Mastery tiers
    mastery = conn.execute("""
        SELECT
            SUM(CASE WHEN reps = 0 THEN 1 ELSE 0 END) AS new_items,
            SUM(CASE WHEN reps BETWEEN 1 AND 2 THEN 1 ELSE 0 END) AS learning,
            SUM(CASE WHEN reps >= 3 THEN 1 ELSE 0 END) AS mature
        FROM conjugate_srs
        WHERE lang = ?
    """, (lang,)).fetchone()

    # Average EF
    avg_ef = conn.execute("""
        SELECT ROUND(AVG(ef), 2) AS avg_ef,
               ROUND(AVG(CASE WHEN reps >= 2 THEN ef END), 2) AS avg_ef_mature
        FROM conjugate_srs WHERE lang = ?
    """, (lang,)).fetchone()

    # Per-tense breakdown
    by_tense = conn.execute("""
        SELECT tense,
               COUNT(*) AS total,
               SUM(CASE WHEN next_review <= date('now') THEN 1 ELSE 0 END) AS due_now,
               ROUND(AVG(ef), 2) AS avg_ef,
               ROUND(AVG(interval), 1) AS avg_interval
        FROM conjugate_srs
        WHERE lang = ?
        GROUP BY tense
        ORDER BY due_now DESC
    """, (lang,)).fetchall()

    # Reviews in last 7 days
    recent = conn.execute("""
        SELECT COUNT(*) AS reviews_7d
        FROM conjugate_attempts
        WHERE lang = ? AND created_at >= datetime('now', '-7 days')
    """, (lang,)).fetchone()

    # Verb+pronoun combos never reviewed
    unseen = conn.execute("""
        SELECT COUNT(*) AS unseen
        FROM verbs_ref v
        WHERE v.lang = ?
          AND NOT EXISTS (
              SELECT 1 FROM conjugate_srs cs
              WHERE cs.infinitive = v.infinitive AND cs.lang = v.lang
          )
    """, (lang,)).fetchone()

    conn.close()

    return {
        "queue": dict(queue) if queue else {},
        "mastery": dict(mastery) if mastery else {},
        "avg_ef": dict(avg_ef) if avg_ef else {},
        "by_tense": [dict(r) for r in by_tense],
        "recent": dict(recent) if recent else {},
        "unseen": dict(unseen) if unseen else {},
    }


# ── Public aliases for app.py ───────────────────────────────────────────

update_vocab_srs = _upsert_vocab_srs
update_conjugate_srs = _upsert_conjugate_srs