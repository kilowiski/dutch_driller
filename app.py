"""
Dutch Driller — a no-bullshit Dutch language training app.
Flask + SQLite. All reference data in SQL tables.
"""

import os, re, random, json
from flask import Flask, render_template, request, jsonify, session

from models import (
    init_db,
    record_vocab, record_conjugate,
    vocab_overall, conjugate_overall,
    cefr_progress, conjugate_tense_stats, daily_streak,
    llm_cache_lookup, llm_cache_store,
    get_vocab_words, get_vocab_categories, get_db,
    get_phrases, get_phrase_scenarios,
    get_sentences, get_sentence_levels,
    get_verbs, PRONOUNS, TENSES, TENSE_LABEL,
    conjugate_verb, check_conjugation,
    insert_vocab, insert_verb, insert_phrase, insert_sentence,
    get_table_counts,
)

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
    from models import get_db
    conn = get_db()
    if conn.execute("SELECT COUNT(*) FROM vocab_words").fetchone()[0] == 0:
        from data.vocabulary import VOCABULARY
        conn.executemany("INSERT INTO vocab_words (dutch,english,category,cefr,example) VALUES (?,?,?,?,?)",
                         [(e["dutch"],e["english"],e["category"],e.get("cefr",""),e.get("example","")) for e in VOCABULARY])
    if conn.execute("SELECT COUNT(*) FROM phrases").fetchone()[0] == 0:
        from data.phrases import PHRASES
        conn.executemany("INSERT INTO phrases (dutch,english,scenario,cefr) VALUES (?,?,?,?)",
                         [(p["dutch"],p["english"],p["scenario"],p.get("cefr","")) for p in PHRASES])
    if conn.execute("SELECT COUNT(*) FROM sentences_ref").fetchone()[0] == 0:
        from data.sentences import SENTENCES; import json
        conn.executemany("INSERT INTO sentences_ref (correct_order,english,cefr) VALUES (?,?,?)",
                         [(json.dumps(s["correct"]),s["english"],s.get("cefr","")) for s in SENTENCES])
    if conn.execute("SELECT COUNT(*) FROM verbs_ref").fetchone()[0] == 0:
        from data.verbs import VERBS; import json
        conn.executemany("INSERT INTO verbs_ref (infinitive,english,type,stem,cefr,example,irregular) VALUES (?,?,?,?,?,?,?)",
                         [(v["infinitive"],v["english"],v["type"],v.get("stem",""),v.get("cefr",""),v.get("example",""),
                           json.dumps(v.get("irregular",{}))) for v in VERBS])
    conn.commit(); conn.close()
_seed_if_empty()

# ── LLM config ─────────────────────────────────────────────────────────

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

# ── Lenient answer matching ────────────────────────────────────────────

_ARTICLE_RE = re.compile(r"^(the|a|an)\s+", re.IGNORECASE)
_HINT_RE = re.compile(r"\s*\([^)]*\)\s*$")
_WS_RE = re.compile(r"\s+")

def _normalize(text):
    t = text.strip().lower()
    t = _ARTICLE_RE.sub("", t)
    t = _HINT_RE.sub("", t)
    t = _WS_RE.sub(" ", t).strip().rstrip(",.!?;:")
    return t

def _matches(user_answer, expected):
    u, e = _normalize(user_answer), _normalize(expected)
    return u == e or (u and e and (u in e or e in u))

def _llm_check(dutch, english, expected, user_answer):
    if not DEEPSEEK_KEY:
        return None
    try:
        import urllib.request
        prompt = (
            f'Dutch word: "{dutch}". Expected English translation: "{expected}". '
            f'User answered: "{user_answer}". Is the user\'s answer an acceptable translation? '
            f'Reply with exactly this JSON and nothing else: '
            f'{{"acceptable": true or false, "explanation": "brief reason in one sentence"}}'
        )
        payload = json.dumps({
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a strict Dutch-English language evaluator. Reply only with JSON."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0, "max_tokens": 150,
        }).encode("utf-8")
        req = urllib.request.Request(DEEPSEEK_URL, data=payload, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_KEY}",
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read())
        content = body["choices"][0]["message"]["content"].strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[-1].rsplit("\n", 1)[0]
        return json.loads(content)
    except Exception as e:
        return {"acceptable": False, "explanation": f"(LLM unavailable: {e})"}


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
    direction = request.args.get("direction", "nl_en")
    category = request.args.get("category", "")
    count = int(request.args.get("count", 10))

    pool = get_vocab_words(category) if category else get_vocab_words()
    items = random.sample(pool, min(count, len(pool)))
    random.shuffle(items)

    drill_items = []
    for entry in items:
        dutch, english = entry["dutch"], entry["english"]
        prompt, answer = (dutch, english) if direction == "nl_en" else (english, dutch)
        drill_items.append({
            "prompt": prompt, "answer": answer,
            "dutch": dutch, "english": english,
            "category": entry["category"],
            "cefr": entry.get("cefr", ""),
            "example": entry.get("example", ""),
        })

    return render_template(
        "vocab.html", items=drill_items, direction=direction,
        categories=get_vocab_categories(), selected_category=category,
    )


@app.route("/vocab/check", methods=["POST"])
def vocab_check():
    data = request.get_json()
    user_answer = data.get("answer", "").strip()
    dutch = data.get("dutch", "")
    english = data.get("english", "")
    category = data.get("category", "")
    cefr = data.get("cefr", "")
    direction = data.get("direction", "nl_en")

    expected = english if direction == "nl_en" else dutch
    correct = _matches(user_answer, expected)
    record_vocab(dutch, english, category, user_answer, correct, direction, cefr)

    return jsonify({
        "correct": correct, "expected": expected,
        "llm_available": bool(DEEPSEEK_KEY and not correct),
    })


def _explain_with_cache(dutch, english, expected, user_answer):
    cached = llm_cache_lookup(dutch, expected, user_answer)
    if cached:
        return cached
    result = _llm_check(dutch, english, expected, user_answer)
    if result:
        llm_cache_store(dutch, expected, user_answer,
                        result.get("acceptable", False),
                        result.get("explanation", ""))
    return result or {"acceptable": False, "explanation": "LLM check failed."}


@app.route("/vocab/explain", methods=["POST"])
def vocab_explain():
    if not DEEPSEEK_KEY:
        return jsonify({"acceptable": False, "explanation": "LLM not configured."})
    data = request.get_json()
    return jsonify(_explain_with_cache(
        dutch=data.get("dutch", ""), english=data.get("english", ""),
        expected=data.get("expected", ""), user_answer=data.get("answer", ""),
    ))


# ── Phrases drill ──────────────────────────────────────────────────────

@app.route("/phrases")
def phrases_drill():
    scenario = request.args.get("scenario", "")
    direction = request.args.get("direction", "nl_en")
    count = int(request.args.get("count", 10))

    pool = get_phrases(scenario) if scenario else get_phrases()
    items = random.sample(pool, min(count, len(pool)))
    random.shuffle(items)

    drill_items = []
    for entry in items:
        dutch, english = entry["dutch"], entry["english"]
        prompt, answer = (dutch, english) if direction == "nl_en" else (english, dutch)
        drill_items.append({
            "prompt": prompt, "answer": answer,
            "dutch": dutch, "english": english,
            "scenario": entry["scenario"], "cefr": entry.get("cefr", ""),
        })

    return render_template(
        "phrases.html", items=drill_items, direction=direction,
        scenarios=get_phrase_scenarios(), selected_scenario=scenario,
    )


@app.route("/phrases/check", methods=["POST"])
def phrases_check():
    data = request.get_json()
    user_answer = data.get("answer", "").strip()
    dutch = data.get("dutch", "")
    english = data.get("english", "")
    expected = english if data.get("direction") == "nl_en" else dutch
    correct = _matches(user_answer, expected)
    record_vocab(dutch, english, "phrases", user_answer, correct,
                 data.get("direction", "nl_en"), data.get("cefr", ""))
    return jsonify({"correct": correct, "expected": expected,
                    "llm_available": bool(DEEPSEEK_KEY and not correct)})


@app.route("/phrases/explain", methods=["POST"])
def phrases_explain():
    if not DEEPSEEK_KEY:
        return jsonify({"acceptable": False, "explanation": "LLM not configured."})
    data = request.get_json()
    return jsonify(_explain_with_cache(
        dutch=data.get("dutch", ""), english=data.get("english", ""),
        expected=data.get("expected", ""), user_answer=data.get("answer", ""),
    ))


# ── Sentence builder drill ─────────────────────────────────────────────

@app.route("/sentences")
def sentence_drill():
    level = request.args.get("level", "")
    count = int(request.args.get("count", 5))

    rows = get_sentences(level) if level else get_sentences()
    items = random.sample(rows, min(count, len(rows)))
    random.shuffle(items)
    for item in items:
        item["correct"] = item.pop("correct_order")

    return render_template("sentences.html", items=items,
                           cefr_levels=get_sentence_levels(), selected_level=level)


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
    tense = request.args.get("tense", "present")
    count = int(request.args.get("count", 10))

    pronouns = list(PRONOUNS.keys())
    pool = get_verbs()
    random.shuffle(pool)

    drill_items = []
    for verb in pool[:count]:
        pronoun = random.choice(pronouns)
        correct_form = conjugate_verb(verb, tense, pronoun)
        drill_items.append({
            "infinitive": verb["infinitive"],
            "english": verb["english"],
            "tense": tense,
            "pronoun": pronoun,
            "pronoun_label": PRONOUNS[pronoun],
            "correct_form": correct_form,
            "cefr": verb.get("cefr", ""),
            "example": verb.get("example", ""),
        })

    return render_template("conjugate.html", items=drill_items, tense=tense,
                           tense_label=TENSE_LABEL.get(tense, tense), tenses=TENSES)


@app.route("/conjugate/check", methods=["POST"])
def conjugate_check():
    data = request.get_json()
    user_answer = data.get("answer", "").strip()
    infinitive = data.get("infinitive", "")
    tense = data.get("tense", "present")
    pronoun = data.get("pronoun", "")

    verbs = get_verbs()
    verb_entry = next((v for v in verbs if v["infinitive"] == infinitive), None)
    if not verb_entry:
        return jsonify({"correct": False, "expected": "?"})

    is_correct, correct_form = check_conjugation(verb_entry, tense, pronoun, user_answer)
    record_conjugate(infinitive, tense, pronoun, user_answer, is_correct)
    return jsonify({"correct": is_correct, "expected": correct_form})


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
    if not DEEPSEEK_KEY:
        return jsonify({"error": "DEEPSEEK_API_KEY not set"}), 400

    data = request.get_json()
    content_type = data.get("type", "vocab")  # vocab, verb, phrase, sentence
    level = data.get("level", "A1")
    count = min(int(data.get("count", 5)), 10)
    category = data.get("category", "")

    # Get existing content to avoid duplicates
    import urllib.request
    if content_type == "vocab":
        existing = [w["dutch"] for w in get_vocab_words()]
        prompt = (
            f"Generate {count} new Dutch vocabulary words at CEFR level {level}."
            + (f" Category theme: {category}." if category else "")
            + f" Do NOT include any of these existing words: {', '.join(existing[:50])}."
            + f" For each word provide: dutch (with article de/het), english, category (one word),"
            + f" and example (a simple Dutch sentence using the word)."
            + f" Reply ONLY with a JSON array of objects like: "
            + f'[{{"dutch":"de hond","english":"the dog","category":"animals","example":"De hond speelt in de tuin."}}]'
        )
    elif content_type == "verb":
        existing = [v["infinitive"] for v in get_verbs()]
        prompt = (
            f"Generate {count} new Dutch verbs at CEFR level {level}."
            + f" Do NOT include: {', '.join(existing)}."
            + f" For each provide: infinitive, english, type (regular/irregular/modal), stem (infinitive minus -en),"
            + f" example (simple Dutch sentence in present tense), and irregular forms (empty object for regular,"
            + f" or e.g. for past: {{'past':{{'ik':'...','wij':'...'}}}} for irregular)."
            + f" Reply ONLY with a JSON array: [{{'infinitive':'...','english':'...','type':'regular','stem':'...','example':'...','irregular':{{}}}}]"
        )
    elif content_type == "phrase":
        existing = [p["dutch"] for p in get_phrases()]
        prompt = (
            f"Generate {count} new Dutch survival phrases at level {level}."
            + f" Do NOT include: {', '.join(existing)}."
            + f" For each provide: dutch, english, scenario (one of: restaurant, shopping, travel, smalltalk, emergency, daily)."
            + f" Reply ONLY with a JSON array: [{{'dutch':'...','english':'...','scenario':'...'}}]"
        )
    else:  # sentence
        existing = [s["english"] for s in get_sentences()]
        prompt = (
            f"Generate {count} new Dutch sentence-ordering exercises at level {level}."
            + f" Do NOT include English sentences like: {', '.join(existing[:30])}."
            + f" For each provide: correct (array of words in correct Dutch order), english translation."
            + f" Reply ONLY with a JSON array: [{{'correct':['Ik','ga','naar','huis'],'english':'I go home'}}]"
        )

    try:
        payload = json.dumps({
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a Dutch language teacher. Reply ONLY with valid JSON arrays. No markdown, no explanation."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7, "max_tokens": 2000,
        }).encode("utf-8")
        req = urllib.request.Request(DEEPSEEK_URL, data=payload, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_KEY}",
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read())
        content = body["choices"][0]["message"]["content"].strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[-1].rsplit("```", 1)[0]
        items = json.loads(content)

        inserted = 0
        for item in items:
            try:
                if content_type == "vocab":
                    insert_vocab(item["dutch"], item["english"], item.get("category", "general"),
                                 level, item.get("example", ""))
                elif content_type == "verb":
                    insert_verb(item["infinitive"], item["english"], item.get("type", "regular"),
                                item.get("stem", item["infinitive"][:-2]), level,
                                item.get("example", ""), item.get("irregular", {}))
                elif content_type == "phrase":
                    insert_phrase(item["dutch"], item["english"],
                                  item.get("scenario", "daily"), level)
                else:
                    insert_sentence(item["correct"], item["english"], level)
                inserted += 1
            except Exception:
                pass

        return jsonify({"success": True, "generated": len(items), "inserted": inserted})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5080)
