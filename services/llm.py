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
    """Generate new content via LLM. get_existing is a callback to get current items to avoid."""
    if not _get_key():
        return None, "DEEPSEEK_API_KEY not set"

    existing = get_existing()

    if content_type == "vocab":
        prompt = (
            f"Generate {count} new {lang_name} vocabulary words at CEFR level {level}."
            + (f" Category theme: {category}." if category else "")
            + f" Do NOT include any of these existing words: {', '.join(existing[:200])}."
            + f" For each word provide: word (the {lang_name} word with article), translation (English), category (one word),"
            + f" and example (a simple {lang_name} sentence using the word)."
            + f" Reply ONLY with a JSON array of objects."
        )
    elif content_type == "verb":
        prompt = (
            f"Generate {count} new {lang_name} verbs at CEFR level {level}."
            + f" Do NOT include: {', '.join(existing)}."
            + f" For each provide: infinitive, translation (English meaning), type (regular/irregular), stem,"
            + f" example, and irregular forms (empty object for regular)."
            + f" Reply ONLY with a JSON array."
        )
    elif content_type == "phrase":
        prompt = (
            f"Generate {count} new {lang_name} survival phrases at level {level}."
            + f" Do NOT include: {', '.join(existing)}."
            + f" For each provide: word ({lang_name} phrase), translation (English), scenario (restaurant/shopping/travel/smalltalk/emergency/daily)."
            + f" Reply ONLY with a JSON array."
        )
    else:  # sentence
        prompt = (
            f"Generate {count} new {lang_name} sentence-ordering exercises at level {level}."
            + f" Do NOT include English sentences like: {', '.join(existing[:100])}."
            + f" For each provide: correct (array of words in correct {lang_name} order), english."
            + f" Reply ONLY with a JSON array."
        )

    try:
        payload = json.dumps({
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": f"You are a {lang_name} language teacher. Reply ONLY with valid JSON arrays. No markdown, no explanation."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7, "max_tokens": 2000,
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
        return json.loads(content), None
    except Exception as e:
        return None, str(e)
