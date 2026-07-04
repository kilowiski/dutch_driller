"""
Dutch Driller — a no-bullshit Dutch language training app.
Flask + SQLite. Two drills: vocabulary and verb conjugation.
"""

import os
import re
import random
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, session

from models import init_db, record_vocab, record_conjugate, vocab_overall, conjugate_overall
from data.verbs import VERBS, PRONOUNS, TENSES, TENSE_LABEL, conjugate, check_answer
from data.vocabulary import VOCABULARY, CATEGORIES, BY_CATEGORY

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dutch-driller-dev-key")

# ── Bootstrap ──────────────────────────────────────────────────────────

def _load_dotenv(path=".env"):
    """Load KEY=VALUE pairs from a .env file (no pip dep)."""
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

# ── LLM config ─────────────────────────────────────────────────────────

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"


# ── Lenient answer matching ────────────────────────────────────────────

_ARTICLE_RE = re.compile(r"^(the|a|an)\s+", re.IGNORECASE)
_HINT_RE = re.compile(r"\s*\([^)]*\)\s*$")
_WS_RE = re.compile(r"\s+")

def _normalize(text):
    """Normalize for comparison: lowercase, strip articles, collapse whitespace."""
    t = text.strip().lower()
    t = _ARTICLE_RE.sub("", t)
    t = _HINT_RE.sub("", t)
    t = _WS_RE.sub(" ", t).strip()
    t = t.rstrip(",.!?;:")
    return t


def _matches(user_answer, expected):
    """Check if user answer matches expected, with lenient rules."""
    u = _normalize(user_answer)
    e = _normalize(expected)
    if u == e:
        return True
    # also accept if user answer is contained in expected or vice versa
    if u and e:
        if u in e or e in u:
            return True
    return False


def _llm_check(dutch, english, expected, user_answer):
    """Ask LLM whether the user's answer is an acceptable translation."""
    if not DEEPSEEK_KEY:
        return None
    try:
        import urllib.request
        prompt = (
            f'Dutch word: "{dutch}". Expected English translation: "{expected}". '
            f'User answered: "{user_answer}". '
            f'Is the user\'s answer an acceptable translation? '
            f'Reply with exactly this JSON and nothing else: '
            f'{{"acceptable": true or false, "explanation": "brief reason in one sentence"}}'
        )
        payload = json.dumps({
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a strict Dutch-English language evaluator. Reply only with JSON."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
            "max_tokens": 150,
        }).encode("utf-8")
        req = urllib.request.Request(DEEPSEEK_URL, data=payload, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_KEY}",
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read())
        content = body["choices"][0]["message"]["content"].strip()
        # Strip markdown code fences if the model wraps it
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
    v_total = vo["total"] or 0
    v_correct = vo["correct_count"] or 0
    c_total = co["total"] or 0
    c_correct = co["correct_count"] or 0

    return render_template(
        "index.html",
        vocab_total=v_total,
        vocab_pct=round(100 * v_correct / v_total) if v_total else 0,
        conj_total=c_total,
        conj_pct=round(100 * c_correct / c_total) if c_total else 0,
    )


# ── Vocabulary drill ─────────────────────────────────────────────────

@app.route("/vocab")
def vocab_drill():
    direction = request.args.get("direction", "nl_en")
    category = request.args.get("category", "")
    count = int(request.args.get("count", 10))

    # Filter by category if specified
    pool = BY_CATEGORY.get(category) if category in BY_CATEGORY else VOCABULARY

    # Grab a random sample
    items = random.sample(pool, min(count, len(pool)))

    # Shuffle to vary order
    random.shuffle(items)

    drill_items = []
    for dutch, english, cat in items:
        if direction == "nl_en":
            prompt = dutch
            answer = english
        else:
            prompt = english
            answer = dutch
        drill_items.append({
            "prompt": prompt,
            "answer": answer,
            "dutch": dutch,
            "english": english,
            "category": cat,
        })

    session["vocab_drill"] = drill_items
    session["vocab_direction"] = direction

    return render_template(
        "vocab.html",
        items=drill_items,
        direction=direction,
        categories=CATEGORIES,
        selected_category=category,
    )


@app.route("/vocab/check", methods=["POST"])
def vocab_check():
    """Check a single answer via AJAX — lenient matching."""
    data = request.get_json()
    user_answer = data.get("answer", "").strip()
    dutch = data.get("dutch", "")
    english = data.get("english", "")
    category = data.get("category", "")
    direction = data.get("direction", "nl_en")

    expected = english if direction == "nl_en" else dutch
    correct = _matches(user_answer, expected)

    record_vocab(dutch, english, category, user_answer, correct, direction)

    return jsonify({
        "correct": correct,
        "expected": expected,
        "llm_available": bool(DEEPSEEK_KEY and not correct),
    })


@app.route("/vocab/explain", methods=["POST"])
def vocab_explain():
    """Ask the LLM to explain why an answer was wrong."""
    if not DEEPSEEK_KEY:
        return jsonify({"acceptable": False, "explanation": "LLM not configured. Set DEEPSEEK_API_KEY env var."})

    data = request.get_json()
    result = _llm_check(
        dutch=data.get("dutch", ""),
        english=data.get("english", ""),
        expected=data.get("expected", ""),
        user_answer=data.get("answer", ""),
    )
    return jsonify(result or {"acceptable": False, "explanation": "LLM check failed."})


# ── Conjugation drill ─────────────────────────────────────────────────

@app.route("/conjugate")
def conjugate_drill():
    tense = request.args.get("tense", "present")
    count = int(request.args.get("count", 10))

    pronouns = list(PRONOUNS.keys())
    pool = VERBS.copy()
    random.shuffle(pool)

    drill_items = []
    for verb in pool[:count]:
        pronoun = random.choice(pronouns)
        correct_form = conjugate(verb, tense, pronoun)
        drill_items.append({
            "infinitive": verb["infinitive"],
            "english": verb["english"],
            "tense": tense,
            "pronoun": pronoun,
            "pronoun_label": PRONOUNS[pronoun],
            "correct_form": correct_form,
        })

    session["conjugate_drill"] = drill_items
    session["conjugate_tense"] = tense

    return render_template(
        "conjugate.html",
        items=drill_items,
        tense=tense,
        tense_label=TENSE_LABEL.get(tense, tense),
        tenses=TENSES,
    )


@app.route("/conjugate/check", methods=["POST"])
def conjugate_check():
    """Check a single answer via AJAX."""
    data = request.get_json()
    user_answer = data.get("answer", "").strip()
    infinitive = data.get("infinitive", "")
    tense = data.get("tense", "present")
    pronoun = data.get("pronoun", "")

    # Find the verb entry
    verb_entry = next((v for v in VERBS if v["infinitive"] == infinitive), None)
    if not verb_entry:
        return jsonify({"correct": False, "expected": "?"})

    is_correct, correct_form = check_answer(verb_entry, tense, pronoun, user_answer)
    record_conjugate(infinitive, tense, pronoun, user_answer, is_correct)

    return jsonify({"correct": is_correct, "expected": correct_form})


# ── Main ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5080)
