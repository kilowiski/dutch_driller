"""
Lenient answer matching for vocab/phrase drills.
Strips articles, parenthetical hints, normalizes whitespace.
"""

import re

_ARTICLE_RE = re.compile(r"^(the|a|an)\s+", re.IGNORECASE)
_HINT_RE = re.compile(r"\s*\([^)]*\)\s*$")
_WS_RE = re.compile(r"\s+")


def normalize(text):
    t = text.strip().lower()
    t = _ARTICLE_RE.sub("", t)
    t = _HINT_RE.sub("", t)
    t = _WS_RE.sub(" ", t).strip().rstrip(",.!?;:")
    return t


def matches(user_answer, expected):
    u, e = normalize(user_answer), normalize(expected)
    return u == e or (u and e and (u in e or e in u))
