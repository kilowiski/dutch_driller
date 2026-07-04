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


# ── Reference data tables + seed (vocab/phrases/sentences) ─────────────

def _ensure_ref_tables():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS vocab_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT, dutch TEXT NOT NULL UNIQUE,
            english TEXT NOT NULL, category TEXT NOT NULL,
            cefr TEXT NOT NULL DEFAULT '', example TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS phrases (
            id INTEGER PRIMARY KEY AUTOINCREMENT, dutch TEXT NOT NULL UNIQUE,
            english TEXT NOT NULL, scenario TEXT NOT NULL,
            cefr TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS sentences_ref (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            correct_order TEXT NOT NULL, english TEXT NOT NULL,
            cefr TEXT NOT NULL DEFAULT ''
        );
    """)
    conn.commit()
    conn.close()


def get_vocab_words(category=None):
    conn = get_db(); _ensure_ref_tables()
    rows = conn.execute("SELECT * FROM vocab_words" + (" WHERE category=?" if category else ""),
                        (category,) if category else ()).fetchall()
    conn.close(); return [dict(r) for r in rows]

def get_vocab_categories():
    conn = get_db()
    rows = conn.execute("SELECT DISTINCT category FROM vocab_words ORDER BY category").fetchall()
    conn.close(); return [r["category"] for r in rows]

def get_phrases(scenario=None):
    conn = get_db(); _ensure_ref_tables()
    rows = conn.execute("SELECT * FROM phrases" + (" WHERE scenario=?" if scenario else ""),
                        (scenario,) if scenario else ()).fetchall()
    conn.close(); return [dict(r) for r in rows]

def get_phrase_scenarios():
    conn = get_db()
    rows = conn.execute("SELECT DISTINCT scenario FROM phrases ORDER BY scenario").fetchall()
    conn.close(); return [r["scenario"] for r in rows]

def get_sentences(level=None):
    conn = get_db(); _ensure_ref_tables()
    rows = conn.execute("SELECT * FROM sentences_ref" + (" WHERE cefr=?" if level else ""),
                        (level,) if level else ()).fetchall()
    conn.close()
    import json
    return [{**dict(r), "correct_order": json.loads(r["correct_order"])} for r in rows]

def get_sentence_levels():
    conn = get_db()
    rows = conn.execute("SELECT DISTINCT cefr FROM sentences_ref ORDER BY cefr").fetchall()
    conn.close(); return [r["cefr"] for r in rows]


# ── Content insert helpers (for runtime additions) ────────────────────

def insert_vocab(dutch, english, category, cefr, example):
    conn = get_db(); _ensure_ref_tables()
    try:
        conn.execute("INSERT INTO vocab_words (dutch, english, category, cefr, example) VALUES (?,?,?,?,?)",
                     (dutch, english, category, cefr, example))
        conn.commit()
    except: pass  # skip duplicates
    conn.close()

def insert_verb(infinitive, english, vtype, stem, cefr, example, irregular):
    conn = get_db(); _ensure_verbs_table()
    import json
    try:
        conn.execute("INSERT INTO verbs_ref (infinitive, english, type, stem, cefr, example, irregular) VALUES (?,?,?,?,?,?,?)",
                     (infinitive, english, vtype, stem, cefr, example, json.dumps(irregular or {})))
        conn.commit()
    except: pass
    conn.close()

def insert_phrase(dutch, english, scenario, cefr):
    conn = get_db(); _ensure_ref_tables()
    try:
        conn.execute("INSERT INTO phrases (dutch, english, scenario, cefr) VALUES (?,?,?,?)",
                     (dutch, english, scenario, cefr))
        conn.commit()
    except: pass
    conn.close()

def insert_sentence(correct_order, english, cefr):
    conn = get_db(); _ensure_ref_tables()
    import json
    try:
        conn.execute("INSERT INTO sentences_ref (correct_order, english, cefr) VALUES (?,?,?)",
                     (json.dumps(correct_order), english, cefr))
        conn.commit()
    except: pass
    conn.close()

def get_table_counts():
    conn = get_db()
    return {
        "vocab": conn.execute("SELECT COUNT(*) FROM vocab_words").fetchone()[0],
        "verbs": conn.execute("SELECT COUNT(*) FROM verbs_ref").fetchone()[0],
        "phrases": conn.execute("SELECT COUNT(*) FROM phrases").fetchone()[0],
        "sentences": conn.execute("SELECT COUNT(*) FROM sentences_ref").fetchone()[0],
    }


# ── Verb reference data + conjugation engine ───────────────────────────

def _ensure_verbs_table():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS verbs_ref (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            infinitive TEXT NOT NULL UNIQUE,
            english    TEXT NOT NULL,
            type       TEXT NOT NULL,
            stem       TEXT NOT NULL DEFAULT '',
            cefr       TEXT NOT NULL DEFAULT '',
            example    TEXT NOT NULL DEFAULT '',
            irregular  TEXT NOT NULL DEFAULT '{}'
        );
    """)
    conn.commit()
    conn.close()


def get_verbs():
    conn = get_db()
    _ensure_verbs_table()
    import json
    rows = conn.execute("SELECT * FROM verbs_ref").fetchall()
    conn.close()
    return [{**dict(r), "irregular": json.loads(r["irregular"])} for r in rows]


# ── Conjugation engine ───────────────────────────────────────────────

PRONOUNS = {"ik":"I","jij":"you (sg inf)","u":"you (formal)","hij":"he","zij":"she","het":"it","wij":"we","jullie":"you (pl)","zij_pl":"they"}
TENSES = ["present","past","perfect"]
TENSE_LABEL = {"present":"present tense (tegenwoordige tijd)","past":"simple past (onvoltooid verleden tijd)","perfect":"present perfect (voltooid tegenwoordige tijd)"}

def _reg_present(stem, pronoun):
    if pronoun=="ik": return stem
    if pronoun in ("jij","u","hij","zij","het"): return stem+"t"
    return stem

def _reg_past(stem, pronoun):
    soft=set("tkfschp"); suffix=stem[-1] in soft if stem else False
    sg = "te" if suffix else "de"; pl = "ten" if suffix else "den"
    return stem+sg if pronoun in ("ik","jij","u","hij","zij","het") else stem+pl

def _reg_perfect(stem):
    soft=set("tkfschp"); suffix = "t" if (stem[-1] in soft if stem else False) else "d"
    return "ge"+stem+suffix

def conjugate_verb(verb_entry, tense, pronoun):
    irr = verb_entry.get("irregular",{})
    if isinstance(irr, str): import json; irr = json.loads(irr)
    if tense in irr and pronoun in irr[tense]: return irr[tense][pronoun]
    stem = verb_entry.get("stem","")
    if tense=="present": return _reg_present(stem, pronoun)
    if tense=="past": return _reg_past(stem, pronoun)
    if tense=="perfect": return _reg_perfect(stem)
    return "?"

def check_conjugation(verb_entry, tense, pronoun, user_answer):
    correct = conjugate_verb(verb_entry, tense, pronoun)
    alts = [a.strip().lower() for a in correct.split("/")]
    return user_answer.strip().lower() in alts, correct


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
