"""
LLM utilities: explain wrong answers (with cache), generate new content.
"""

import os, json, urllib.request
from models import llm_cache_lookup, llm_cache_store

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

def _get_key():
    return os.environ.get("DEEPSEEK_API_KEY", "")


def _llm_check(word, translation, expected, user_answer, lang_name="Dutch"):
    """Ask LLM whether the user's answer is an acceptable translation."""
    if not _get_key():
        return None
    try:
        prompt = (
            f'{lang_name} word: "{word}". Expected English translation: "{expected}". '
            f'User answered: "{user_answer}". Is the user\'s answer an acceptable translation? '
            f'Reply with exactly this JSON and nothing else: '
            f'{{"acceptable": true or false, "explanation": "brief reason in one sentence"}}'
        )
        payload = json.dumps({
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": f"You are a strict {lang_name}-English language evaluator. Reply only with JSON."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0, "max_tokens": 150,
        }).encode("utf-8")
        req = urllib.request.Request(DEEPSEEK_URL, data=payload, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {_get_key()}",
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read())
        content = body["choices"][0]["message"]["content"].strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[-1].rsplit("```", 1)[0]
        return json.loads(content)
    except Exception as e:
        return {"acceptable": False, "explanation": f"(LLM unavailable: {e})"}


def explain(word, translation, expected, user_answer, lang_name="Dutch"):
    """Look up in cache, call LLM if needed, store result."""
    if not _get_key():
        return {"acceptable": False, "explanation": "LLM not configured. Set DEEPSEEK_API_KEY env var."}
    cached = llm_cache_lookup(word, expected, user_answer)
    if cached:
        return cached
    result = _llm_check(word, translation, expected, user_answer, lang_name)
    if result:
        llm_cache_store(word, expected, user_answer,
                        result.get("acceptable", False),
                        result.get("explanation", ""))
    return result or {"acceptable": False, "explanation": "LLM check failed."}


def generate(content_type, level, count, category, get_existing, lang_name="Dutch"):
    """Generate new content via LLM with duplicate guard. Retries until count is reached."""
    if not _get_key():
        return None, "DEEPSEEK_API_KEY not set"

    # Key extractors for dedup
    if content_type == "vocab":
        key_fn = lambda item: item.get("word", "").strip().lower()
    elif content_type == "verb":
        key_fn = lambda item: item.get("infinitive", "").strip().lower()
    elif content_type == "phrase":
        key_fn = lambda item: item.get("word", "").strip().lower()
    else:
        key_fn = lambda item: item.get("english", "").strip().lower()

    collected = []
    seen_keys = set()
    existing = set(k.lower() for k in get_existing())
    seen_keys.update(existing)

    max_retries = 4
    for attempt in range(max_retries):
        needed = count - len(collected)
        if needed <= 0:
            break

        existing_list = ', '.join(sorted(existing))
        prompt = _build_prompt(content_type, needed, level, category, existing_list, lang_name)

        try:
            items = _call_llm(prompt, lang_name)
            if not items:
                break

            for item in items:
                key = key_fn(item)
                if key and key not in seen_keys:
                    seen_keys.add(key)
                    collected.append(item)
                    if len(collected) >= count:
                        break

            # Refresh existing list for next attempt (includes what we just added)
            existing = set(k.lower() for k in get_existing())
            existing.update(seen_keys)
        except Exception:
            break

    return collected, None


def _build_prompt(content_type, count, level, category, existing_list, lang_name):
    if content_type == "vocab":
        return (
            f"Generate {count} brand-new {lang_name} vocabulary words at CEFR level {level}."
            + (f" Category theme: {category}." if category else "")
            + f" These words ALREADY EXIST — do NOT repeat any of them: {existing_list}."
            + f" You MUST generate words that are NOT in that list."
            + f" For each word provide: word (the {lang_name} word with article), translation (English), category (one word),"
            + f" and example (a simple {lang_name} sentence using the word)."
            + f" Reply ONLY with a JSON array of objects."
        )
    elif content_type == "verb":
        return (
            f"Generate {count} new {lang_name} verbs at CEFR level {level}."
            + f" Do NOT include: {existing_list}."
            + f" For each provide: infinitive, translation (English meaning), type (regular/irregular), stem,"
            + f" example, and irregular forms (empty object for regular)."
            + f" Reply ONLY with a JSON array."
        )
    elif content_type == "phrase":
        return (
            f"Generate {count} new {lang_name} survival phrases at level {level}."
            + f" Do NOT include: {existing_list}."
            + f" For each provide: word ({lang_name} phrase), translation (English), scenario (restaurant/shopping/travel/smalltalk/emergency/daily)."
            + f" Reply ONLY with a JSON array."
        )
    else:
        return (
            f"Generate {count} new {lang_name} sentence-ordering exercises at level {level}."
            + f" Do NOT include English sentences like: {existing_list}."
            + f" For each provide: correct (array of words in correct {lang_name} order), english."
            + f" Reply ONLY with a JSON array."
        )


def _call_llm(prompt, lang_name):
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": f"You are a {lang_name} language teacher. Reply ONLY with valid JSON arrays. No markdown, no explanation."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.9, "max_tokens": 4000,
    }).encode("utf-8")
    req = urllib.request.Request(DEEPSEEK_URL, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {_get_key()}",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read())
    content = body["choices"][0]["message"]["content"].strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[-1].rsplit("```", 1)[0]
    return json.loads(content)
