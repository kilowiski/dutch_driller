"""
Language registry for Dutch Driller.

To add a new language:
  1. Add an entry to LANGUAGES below.
  2. Create data/{lang}_vocabulary.py, data/{lang}_verbs.py, etc.
  3. Create engines/{lang}.py subclassing ConjugationEngine.
  4. That's it — routes, templates, and SRS adapt automatically.

Direction convention:
  forward  = show target-language word, expect English translation
  reverse  = show English, expect target-language word
"""

LANGUAGES = {
    "nl": {
        "code": "nl",
        "name": "Dutch",
        "native_name": "Nederlands",
        "flag": "🇳🇱",
    },
    # "es": {
    #     "code": "es",
    #     "name": "Spanish",
    #     "native_name": "Español",
    #     "flag": "🇪🇸",
    # },
}

DEFAULT_LANG = "nl"
DIRECTIONS = ("forward", "reverse")


def get_lang(lang_code=None):
    """Return language config dict, falling back to default."""
    code = lang_code or DEFAULT_LANG
    return LANGUAGES.get(code, LANGUAGES[DEFAULT_LANG])


def available_languages():
    """Return list of all supported language codes + names."""
    return [(code, cfg["name"]) for code, cfg in LANGUAGES.items()]
