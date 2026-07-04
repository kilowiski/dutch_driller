"""
Dutch Driller — a no-bullshit language training app.
Flask + SQLite. All reference data in SQL tables.
Supports multiple languages via the LANGUAGES registry.
"""

import os, random, json
from flask import Flask, render_template, request, jsonify, session

from models import (
    init_db,
    record_vocab, record_conjugate,
    vocab_overall, conjugate_overall,
    cefr_progress, conjugate_tense_stats, daily_streak,
    get_vocab_words, get_vocab_categories, get_db,
    get_phrases, get_phrase_scenarios,
    get_sentences, get_sentence_levels,
    insert_vocab, insert_verb, insert_phrase, insert_sentence,
    get_table_counts,
    get_due_vocab, get_due_phrases, get_due_conjugations,
    update_vocab_srs, update_conjugate_srs,
    srs_vocab_stats, srs_conjugate_stats,
)

from languages import get_lang, DEFAULT_LANG, available_languages
from engines.dutch import DutchEngine
from services.matching import matches
from services.llm import explain, generate as llm_generate

# ── Engine registry ─────────────────────────────────────────────────────
# Maps lang code → engine instance.  Add new languages here.
ENGINES = {
    "nl": DutchEngine(),
}


def get_engine(lang):
    """Return the conjugation engine for a language, falling back to Dutch."""
    return ENGINES.get(lang, ENGINES[DEFAULT_LANG])


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dutch-driller-dev-key")

# ── Bootstrap ──────────────────────────────────────────────────────────

def _load_dotenv(path=".env"):
    fp = os.path.join(os.path.dirname(__file__), path)
    if not os.path.isfile(fp):
        return
    with open(fp, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k not in os.environ:
                os.environ[k] = v

_load_dotenv()
init_db()

# One-time seed: populate from .py files if tables are empty
def _seed_if_empty():
    try:
        conn = get_db()
        if conn.execute("SELECT COUNT(*) FROM vocab_words").fetchone()[0] == 0:
            from data.vocabulary import VOCABULARY
            conn.executemany(
                "INSERT INTO vocab_words (word, translation, category, lang, cefr, example) VALUES (?,?,?,?,?,?)",
                [(e["word"], e["translation"], e["category"], e.get("lang", "nl"), e.get("cefr", ""), e.get("example", ""))
                 for e in VOCABULARY],
            )
        if conn.execute("SELECT COUNT(*) FROM phrases").fetchone()[0] == 0:
            from data.phrases import PHRASES
            conn.executemany(
                "INSERT INTO phrases (word, translation, scenario, lang, cefr) VALUES (?,?,?,?,?)",
                [(p["word"], p["translation"], p["scenario"], p.get("lang", "nl"), p.get("cefr", ""))
                 for p in PHRASES],
            )
        if conn.execute("SELECT COUNT(*) FROM sentences_ref").fetchone()[0] == 0:
            from data.sentences import SENTENCES
            conn.executemany(
                "INSERT INTO sentences_ref (correct_order, english, lang, cefr) VALUES (?,?,?,?)",
                [(json.dumps(s["correct"]), s["english"], s.get("lang", "nl"), s.get("cefr", ""))
                 for s in SENTENCES],
            )
        if conn.execute("SELECT COUNT(*) FROM verbs_ref").fetchone()[0] == 0:
            from data.verbs import VERBS
            conn.executemany(
                "INSERT INTO verbs_ref (infinitive, translation, type, stem, lang, cefr, example, irregular) VALUES (?,?,?,?,?,?,?,?)",
                [(v["infinitive"], v["translation"], v["type"], v.get("stem", ""), v.get("lang", "nl"),
                  v.get("cefr", ""), v.get("example", ""), json.dumps(v.get("irregular", {})))
                 for v in VERBS],
            )
        conn.commit(); conn.close()
    except Exception:
        pass
_seed_if_empty()


# ── Context processor: inject lang config into all templates ───────────

@app.context_processor
def inject_lang():
    lang = request.args.get("lang", DEFAULT_LANG)
    return {
        "lang": get_lang(lang),
        "lang_code": lang,
        "available_languages": available_languages(),
    }


# ── Home ───────────────────────────────────────────────────────────────

@app.route("/")
def index():
    vo = vocab_overall()
    co = conjugate_overall()
    v_total, v_correct = vo["total"] or 0, vo["correct_count"] or 0
    c_total, c_correct = co["total"] or 0, co["correct_count"] or 0

    conn = get_db()
    rows = conn.execute("SELECT cefr, COUNT(*) as total FROM vocab_words WHERE cefr != '' GROUP BY cefr").fetchall()
    conn.close()
    vocab_totals = {r["cefr"]: r["total"] for r in rows}

    return render_template(
        "index.html",
        vocab_total=v_total,
        vocab_pct=round(100 * v_correct / v_total) if v_total else 0,
        conj_total=c_total,
        conj_pct=round(100 * c_correct / c_total) if c_total else 0,
        cefr_levels=cefr_progress(),
        vocab_totals=vocab_totals,
        tense_stats=conjugate_tense_stats(),
        streak=daily_streak(),
    )


# ── Vocabulary drill ─────────────────────────────────────────────────

@app.route("/vocab")
def vocab_drill():
    lang = request.args.get("lang", DEFAULT_LANG)
    direction = request.args.get("direction", "forward")
    category = request.args.get("category", "")
    count = int(request.args.get("count", 10))

    items = get_due_vocab(direction, lang, category, count)
    random.shuffle(items)

    drill_items = []
    for entry in items:
        word, translation = entry["word"], entry["translation"]
        prompt, answer = (word, translation) if direction == "forward" else (translation, word)
        drill_items.append({
            "prompt": prompt, "answer": answer,
            "word": word, "translation": translation,
            "category": entry["category"],
            "cefr": entry.get("cefr", ""),
            "example": entry.get("example", ""),
        })

    return render_template(
        "vocab.html", items=drill_items, direction=direction,
        categories=get_vocab_categories(lang), selected_category=category,
    )


@app.route("/vocab/check", methods=["POST"])
def vocab_check():
    data = request.get_json()
    user_answer = data.get("answer", "").strip()
    word = data.get("word", "")
    translation = data.get("translation", "")
    category = data.get("category", "")
    cefr = data.get("cefr", "")
    direction = data.get("direction", "forward")
    lang = data.get("lang", DEFAULT_LANG)

    expected = translation if direction == "forward" else word
    correct = matches(user_answer, expected)
    record_vocab(word, translation, category, user_answer, correct, direction, lang, cefr)
    update_vocab_srs(word, direction, lang, correct)

    return jsonify({
        "correct": correct, "expected": expected,
        "llm_available": not correct,
    })


@app.route("/vocab/explain", methods=["POST"])
def vocab_explain():
    data = request.get_json()
    return jsonify(explain(
        dutch=data.get("word", ""), english=data.get("translation", ""),
        expected=data.get("expected", ""), user_answer=data.get("answer", ""),
    ))


# ── Phrases drill ──────────────────────────────────────────────────────

@app.route("/phrases")
def phrases_drill():
    lang = request.args.get("lang", DEFAULT_LANG)
    scenario = request.args.get("scenario", "")
    direction = request.args.get("direction", "forward")
    count = int(request.args.get("count", 10))

    items = get_due_phrases(direction, lang, scenario, count)
    random.shuffle(items)

    drill_items = []
    for entry in items:
        word, translation = entry["word"], entry["translation"]
        prompt, answer = (word, translation) if direction == "forward" else (translation, word)
        drill_items.append({
            "prompt": prompt, "answer": answer,
            "word": word, "translation": translation,
            "scenario": entry["scenario"], "cefr": entry.get("cefr", ""),
        })

    return render_template(
        "phrases.html", items=drill_items, direction=direction,
        scenarios=get_phrase_scenarios(lang), selected_scenario=scenario,
    )


@app.route("/phrases/check", methods=["POST"])
def phrases_check():
    data = request.get_json()
    user_answer = data.get("answer", "").strip()
    word = data.get("word", "")
    translation = data.get("translation", "")
    direction = data.get("direction", "forward")
    lang = data.get("lang", DEFAULT_LANG)
    expected = translation if direction == "forward" else word
    correct = matches(user_answer, expected)
    record_vocab(word, translation, "phrases", user_answer, correct, direction, lang, data.get("cefr", ""))
    update_vocab_srs(word, direction, lang, correct)
    return jsonify({"correct": correct, "expected": expected,
                    "llm_available": not correct})


@app.route("/phrases/explain", methods=["POST"])
def phrases_explain():
    data = request.get_json()
    return jsonify(explain(
        dutch=data.get("word", ""), english=data.get("translation", ""),
        expected=data.get("expected", ""), user_answer=data.get("answer", ""),
    ))


# ── Sentence builder drill ─────────────────────────────────────────────

@app.route("/sentences")
def sentence_drill():
    lang = request.args.get("lang", DEFAULT_LANG)
    level = request.args.get("level", "")
    count = int(request.args.get("count", 5))

    rows = get_sentences(level, lang) if level else get_sentences(lang=lang)
    items = random.sample(rows, min(count, len(rows)))
    random.shuffle(items)
    for item in items:
        item["correct"] = item.pop("correct_order")

    return render_template("sentences.html", items=items,
                           cefr_levels=get_sentence_levels(lang), selected_level=level)


@app.route("/sentences/check", methods=["POST"])
def sentences_check():
    data = request.get_json()
    user_order = data.get("order", [])
    correct_order = data.get("correct", [])
    correct = user_order == correct_order
    return jsonify({"correct": correct, "correct_order": " ".join(correct_order)})


# ── Conjugation drill ─────────────────────────────────────────────────

@app.route("/conjugate")
def conjugate_drill():
    lang = request.args.get("lang", DEFAULT_LANG)
    tense = request.args.get("tense", "present")
    count = int(request.args.get("count", 10))

    engine = get_engine(lang)
    items = get_due_conjugations(tense, lang, count)

    drill_items = []
    for item in items:
        correct_form = engine.conjugate(item, tense, item["pronoun"])
        drill_items.append({
            "infinitive": item["infinitive"],
            "translation": item["translation"],
            "tense": tense,
            "pronoun": item["pronoun"],
            "pronoun_label": engine.pronouns[item["pronoun"]],
            "correct_form": correct_form,
            "cefr": item.get("cefr", ""),
            "example": item.get("example", ""),
        })

    return render_template("conjugate.html", items=drill_items, tense=tense,
                           tense_label=engine.tense_labels.get(tense, tense),
                           tenses=engine.tenses)


@app.route("/conjugate/check", methods=["POST"])
def conjugate_check():
    data = request.get_json()
    user_answer = data.get("answer", "").strip()
    infinitive = data.get("infinitive", "")
    tense = data.get("tense", "present")
    pronoun = data.get("pronoun", "")
    lang = data.get("lang", DEFAULT_LANG)

    engine = get_engine(lang)
    verbs = engine.get_verbs(lang)
    verb_entry = next((v for v in verbs if v["infinitive"] == infinitive), None)
    if not verb_entry:
        return jsonify({"correct": False, "expected": "?"})

    is_correct, correct_form = engine.check_answer(verb_entry, tense, pronoun, user_answer)
    record_conjugate(infinitive, tense, pronoun, user_answer, is_correct, lang)
    update_conjugate_srs(infinitive, tense, pronoun, lang, is_correct)
    return jsonify({"correct": is_correct, "expected": correct_form})


# ── SRS Stats ──────────────────────────────────────────────────────────

@app.route("/stats")
def stats_page():
    lang = request.args.get("lang", DEFAULT_LANG)
    return render_template(
        "stats.html",
        vocab=srs_vocab_stats(lang),
        conjugate=srs_conjugate_stats(lang),
    )


# ── Admin + Content Generator ──────────────────────────────────────────

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")

def _check_admin():
    return request.args.get("pw", "") == ADMIN_PASSWORD


@app.route("/admin")
def admin_page():
    if not _check_admin():
        return "Unauthorized. Add ?pw=your_password", 401
    counts = get_table_counts()
    return render_template("admin.html", counts=counts, pw=request.args.get("pw", ""))


@app.route("/generate", methods=["POST"])
def generate_content():
    if not _check_admin():
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json()
    content_type = data.get("type", "vocab")
    level = data.get("level", "A1")
    count = min(int(data.get("count", 5)), 10)
    category = data.get("category", "")
    lang = data.get("lang", DEFAULT_LANG)

    if content_type == "vocab":
        get_existing = lambda: [w["word"] for w in get_vocab_words(lang=lang)]
    elif content_type == "verb":
        get_existing = lambda: [v["infinitive"] for v in get_engine(lang).get_verbs(lang)]
    elif content_type == "phrase":
        get_existing = lambda: [p["word"] for p in get_phrases(lang=lang)]
    else:
        get_existing = lambda: [s["english"] for s in get_sentences(lang=lang)]

    items, error = llm_generate(content_type, level, count, category, get_existing)
    if error:
        return jsonify({"error": error}), 400

    inserted = 0
    for item in items:
        try:
            if content_type == "vocab":
                insert_vocab(item["word"], item["translation"], item.get("category", "general"), level, item.get("example", ""), lang)
            elif content_type == "verb":
                insert_verb(item["infinitive"], item["translation"], item.get("type", "regular"),
                            item.get("stem", item["infinitive"][:-2]), level, item.get("example", ""), item.get("irregular", {}), lang)
            elif content_type == "phrase":
                insert_phrase(item["word"], item["translation"], item.get("scenario", "daily"), level, lang)
            else:
                insert_sentence(item["correct"], item["english"], level, lang)
            inserted += 1
        except Exception:
            pass

    return jsonify({"success": True, "generated": len(items), "inserted": inserted})



if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5080)
