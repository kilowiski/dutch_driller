"""
Dutch Driller — a no-bullshit Dutch language training app.
Flask + SQLite. Two drills: vocabulary and verb conjugation.
"""

import os
import random
from flask import Flask, render_template, request, redirect, url_for, jsonify, session

from models import init_db, record_vocab, record_conjugate, vocab_overall, conjugate_overall
from data.verbs import VERBS, PRONOUNS, TENSES, TENSE_LABEL, conjugate, check_answer
from data.vocabulary import VOCABULARY, CATEGORIES, BY_CATEGORY

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dutch-driller-dev-key")

# ── Bootstrap ──────────────────────────────────────────────────────────

init_db()


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
    """Check a single answer via AJAX."""
    data = request.get_json()
    user_answer = data.get("answer", "").strip()
    dutch = data.get("dutch", "")
    english = data.get("english", "")
    category = data.get("category", "")
    direction = data.get("direction", "nl_en")

    expected = english if direction == "nl_en" else dutch
    correct = user_answer.lower() == expected.lower()

    record_vocab(dutch, english, category, user_answer, correct, direction)

    return jsonify({"correct": correct, "expected": expected})


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
