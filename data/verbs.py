"""
Dutch verb bank with conjugation rules.
Supports: present tense (regular + irregular), simple past (imperfectum),
and present perfect (perfectum) for common verbs.
"""

# ── Tense / pronoun mappings ──────────────────────────────────────────────
PRONOUNS = {
    "ik":       "I",
    "jij":      "you (singular, informal)",
    "u":        "you (formal)",
    "hij":      "he",
    "zij":      "she",
    "het":      "it",
    "wij":      "we",
    "jullie":   "you (plural)",
    "zij_pl":   "they",
}

TENSES = ["present", "past", "perfect"]

TENSE_LABEL = {
    "present": "present tense (tegenwoordige tijd)",
    "past":    "simple past (onvoltooid verleden tijd)",
    "perfect": "present perfect (voltooid tegenwoordige tijd)",
}

# ── Regular conjugation helpers ───────────────────────────────────────────

def _regular_present(stem, pronoun):
    """Regular present-tense endings for a given stem."""
    if pronoun == "ik":
        return stem
    elif pronoun in ("jij", "u"):
        return stem + "t"
    elif pronoun in ("hij", "zij", "het"):
        return stem + "t"
    elif pronoun in ("wij", "jullie", "zij_pl"):
        return stem  # infinitive in plural
    return stem

def _regular_past(stem, pronoun, is_soft=False):
    """
    Regular simple past. Soft ketchup rule: stem ending in t,k,f,s,ch,p → -te(n);
    otherwise → -de(n).
    """
    soft_endings = set("tkfschp")  # 't kofschip / soft ketchup
    last = stem[-1] if stem else ""
    suffix_te = last in soft_endings or is_soft

    if pronoun in ("ik", "jij", "u", "hij", "zij", "het"):
        return stem + ("te" if suffix_te else "de")
    else:
        return stem + ("ten" if suffix_te else "den")

def _regular_perfect(stem, is_soft=False):
    """Regular present perfect: ge- + stem + -t/-d."""
    soft_endings = set("tkfschp")
    last = stem[-1] if stem else ""
    suffix_t = last in soft_endings or is_soft
    return "ge" + stem + ("t" if suffix_t else "d")


# ── Verb bank ─────────────────────────────────────────────────────────────
# Each entry:
#   infinitive: Dutch infinitive
#   english:    English meaning
#   type:       "regular" | "irregular" | "modal"
#   stem:       stem for regular verbs (infinitive minus -en, adjusted)
#   irregular:  dict of {tense: {pronoun: form, ...}} for irregular parts
#               (only override what differs from regular)

VERBS = [
    # ── Regular ───────────────────────────────────────────────────────
    {"infinitive": "werken",    "english": "to work",   "type": "regular", "stem": "werk",   "cefr": "A1", "emoji": "💼", "example": "Ik werk vijf dagen per week."},
    {"infinitive": "wonen",     "english": "to live",   "type": "regular", "stem": "woon",   "cefr": "A1", "emoji": "🏠", "example": "Wij wonen in een klein dorp."},
    {"infinitive": "leren",     "english": "to learn",  "type": "regular", "stem": "leer",   "cefr": "A1", "emoji": "📚", "example": "Zij leert Nederlands op school."},
    {"infinitive": "spelen",    "english": "to play",   "type": "regular", "stem": "speel",  "cefr": "A1", "emoji": "⚽", "example": "De kinderen spelen in de tuin."},
    {"infinitive": "koken",     "english": "to cook",   "type": "regular", "stem": "kook",   "cefr": "A1", "emoji": "🍳", "example": "Mijn moeder kookt graag."},
    {"infinitive": "praten",    "english": "to talk",   "type": "regular", "stem": "praat",  "cefr": "A1", "emoji": "💬", "example": "Zij praten over het weer."},
    {"infinitive": "luisteren", "english": "to listen", "type": "regular", "stem": "luister","cefr": "A2", "emoji": "🎧", "example": "Ik luister naar muziek."},
    {"infinitive": "fietsen",   "english": "to cycle",  "type": "regular", "stem": "fiets",  "cefr": "A1", "emoji": "🚲", "example": "Wij fietsen elke dag naar school."},
    {"infinitive": "reizen",    "english": "to travel", "type": "regular", "stem": "reis",   "cefr": "A2", "emoji": "✈️", "example": "Zij reizen graag naar het buitenland."},
    {"infinitive": "dansen",    "english": "to dance",  "type": "regular", "stem": "dans",   "cefr": "A2", "emoji": "💃", "example": "Zij dansen de hele nacht."},
    {"infinitive": "maken",     "english": "to make",   "type": "regular", "stem": "maak",   "cefr": "A1", "emoji": "🔨", "example": "Ik maak het ontbijt klaar."},
    {"infinitive": "huren",     "english": "to rent",   "type": "regular", "stem": "huur",   "cefr": "A2", "emoji": "🏠", "example": "Wij huren een appartement in de stad."},
    {"infinitive": "bellen",    "english": "to call",   "type": "regular", "stem": "bel",    "cefr": "A2", "emoji": "📞", "example": "Ik bel je morgen terug."},
    {"infinitive": "proberen",  "english": "to try",    "type": "regular", "stem": "probeer","cefr": "A2", "emoji": "🎯", "example": "Ik probeer Nederlands te spreken."},
    {"infinitive": "gebruiken", "english": "to use",    "type": "regular", "stem": "gebruik","cefr": "A2", "emoji": "🛠️", "example": "Zij gebruikt haar telefoon veel."},

    # ── Irregular / strong ────────────────────────────────────────────
    {"infinitive": "zijn",      "english": "to be",   "type": "irregular", "cefr": "A1", "emoji": "✨", "example": "Ik ben moe vandaag.",
     "irregular": {
         "present": {"ik": "ben", "jij": "bent", "u": "bent", "hij": "is", "zij": "is", "het": "is",
                     "wij": "zijn", "jullie": "zijn", "zij_pl": "zijn"},
         "past":    {"ik": "was", "jij": "was", "u": "was", "hij": "was", "zij": "was", "het": "was",
                     "wij": "waren", "jullie": "waren", "zij_pl": "waren"},
         "perfect": {"ik": "ben geweest"},
     }},
    {"infinitive": "hebben",    "english": "to have", "type": "irregular", "cefr": "A1", "emoji": "✋", "example": "Ik heb een vraag.",
     "irregular": {
         "present": {"ik": "heb", "jij": "hebt", "u": "hebt", "hij": "heeft", "zij": "heeft", "het": "heeft",
                     "wij": "hebben", "jullie": "hebben", "zij_pl": "hebben"},
         "past":    {"ik": "had", "jij": "had", "u": "had", "hij": "had", "zij": "had", "het": "had",
                     "wij": "hadden", "jullie": "hadden", "zij_pl": "hadden"},
         "perfect": {"ik": "heb gehad"},
     }},
    {"infinitive": "gaan",      "english": "to go",   "type": "irregular", "cefr": "A1", "emoji": "🚶", "example": "Ik ga naar huis.",
     "irregular": {
         "present": {"ik": "ga", "jij": "gaat", "u": "gaat", "hij": "gaat", "zij": "gaat", "het": "gaat",
                     "wij": "gaan", "jullie": "gaan", "zij_pl": "gaan"},
         "past":    {"ik": "ging", "jij": "ging", "u": "ging", "hij": "ging", "zij": "ging", "het": "ging",
                     "wij": "gingen", "jullie": "gingen", "zij_pl": "gingen"},
         "perfect": {"ik": "is gegaan"},
     }},
    {"infinitive": "komen",     "english": "to come",  "type": "irregular", "cefr": "A1", "emoji": "🚪", "example": "Zij komt uit Nederland.",
     "irregular": {
         "present": {"ik": "kom", "jij": "komt", "u": "komt", "hij": "komt", "zij": "komt", "het": "komt",
                     "wij": "komen", "jullie": "komen", "zij_pl": "komen"},
         "past":    {"ik": "kwam", "jij": "kwam", "u": "kwam", "hij": "kwam", "zij": "kwam", "het": "kwam",
                     "wij": "kwamen", "jullie": "kwamen", "zij_pl": "kwamen"},
         "perfect": {"ik": "is gekomen"},
     }},
    {"infinitive": "doen",      "english": "to do",    "type": "irregular", "cefr": "A1", "emoji": "🛠️", "example": "Wat doe je vandaag?",
     "irregular": {
         "present": {"ik": "doe", "jij": "doet", "u": "doet", "hij": "doet", "zij": "doet", "het": "doet",
                     "wij": "doen", "jullie": "doen", "zij_pl": "doen"},
         "past":    {"ik": "deed", "jij": "deed", "u": "deed", "hij": "deed", "zij": "deed", "het": "deed",
                     "wij": "deden", "jullie": "deden", "zij_pl": "deden"},
         "perfect": {"ik": "heb gedaan"},
     }},
    {"infinitive": "zien",      "english": "to see",   "type": "irregular", "cefr": "A1", "emoji": "👀", "example": "Ik zie een vogel in de boom.",
     "irregular": {
         "present": {"ik": "zie", "jij": "ziet", "u": "ziet", "hij": "ziet", "zij": "ziet", "het": "ziet",
                     "wij": "zien", "jullie": "zien", "zij_pl": "zien"},
         "past":    {"ik": "zag", "jij": "zag", "u": "zag", "hij": "zag", "zij": "zag", "het": "zag",
                     "wij": "zagen", "jullie": "zagen", "zij_pl": "zagen"},
         "perfect": {"ik": "heb gezien"},
     }},
    {"infinitive": "geven",     "english": "to give",  "type": "irregular", "cefr": "A2", "emoji": "🎁", "example": "Ik geef je een cadeau.",
     "irregular": {
         "present": {"ik": "geef", "jij": "geeft", "u": "geeft", "hij": "geeft", "zij": "geeft", "het": "geeft",
                     "wij": "geven", "jullie": "geven", "zij_pl": "geven"},
         "past":    {"ik": "gaf", "jij": "gaf", "u": "gaf", "hij": "gaf", "zij": "gaf", "het": "gaf",
                     "wij": "gaven", "jullie": "gaven", "zij_pl": "gaven"},
         "perfect": {"ik": "heb gegeven"},
     }},
    {"infinitive": "nemen",     "english": "to take",  "type": "irregular", "cefr": "A2", "emoji": "✋", "example": "Ik neem de trein naar Utrecht.",
     "irregular": {
         "present": {"ik": "neem", "jij": "neemt", "u": "neemt", "hij": "neemt", "zij": "neemt", "het": "neemt",
                     "wij": "nemen", "jullie": "nemen", "zij_pl": "nemen"},
         "past":    {"ik": "nam", "jij": "nam", "u": "nam", "hij": "nam", "zij": "nam", "het": "nam",
                     "wij": "namen", "jullie": "namen", "zij_pl": "namen"},
         "perfect": {"ik": "heb genomen"},
     }},
    {"infinitive": "eten",      "english": "to eat",   "type": "irregular", "cefr": "A1", "emoji": "🍽️", "example": "Wij eten om zes uur.",
     "irregular": {
         "present": {"ik": "eet", "jij": "eet", "u": "eet", "hij": "eet", "zij": "eet", "het": "eet",
                     "wij": "eten", "jullie": "eten", "zij_pl": "eten"},
         "past":    {"ik": "at", "jij": "at", "u": "at", "hij": "at", "zij": "at", "het": "at",
                     "wij": "aten", "jullie": "aten", "zij_pl": "aten"},
         "perfect": {"ik": "heb gegeten"},
     }},
    {"infinitive": "drinken",   "english": "to drink", "type": "irregular", "cefr": "A1", "emoji": "🥤", "example": "Ik drink koffie in de ochtend.",
     "irregular": {
         "present": {"ik": "drink", "jij": "drinkt", "u": "drinkt", "hij": "drinkt", "zij": "drinkt", "het": "drinkt",
                     "wij": "drinken", "jullie": "drinken", "zij_pl": "drinken"},
         "past":    {"ik": "dronk", "jij": "dronk", "u": "dronk", "hij": "dronk", "zij": "dronk", "het": "dronk",
                     "wij": "dronken", "jullie": "dronken", "zij_pl": "dronken"},
         "perfect": {"ik": "heb gedronken"},
     }},
    {"infinitive": "spreken",   "english": "to speak", "type": "irregular", "cefr": "A1", "emoji": "🗣️", "example": "Spreekt u Nederlands?",
     "irregular": {
         "present": {"ik": "spreek", "jij": "spreekt", "u": "spreekt", "hij": "spreekt", "zij": "spreekt", "het": "spreekt",
                     "wij": "spreken", "jullie": "spreken", "zij_pl": "spreken"},
         "past":    {"ik": "sprak", "jij": "sprak", "u": "sprak", "hij": "sprak", "zij": "sprak", "het": "sprak",
                     "wij": "spraken", "jullie": "spraken", "zij_pl": "spraken"},
         "perfect": {"ik": "heb gesproken"},
     }},
    {"infinitive": "schrijven", "english": "to write", "type": "irregular", "cefr": "A1", "emoji": "✍️", "example": "Ik schrijf een brief.",
     "irregular": {
         "present": {"ik": "schrijf", "jij": "schrijft", "u": "schrijft", "hij": "schrijft", "zij": "schrijft", "het": "schrijft",
                     "wij": "schrijven", "jullie": "schrijven", "zij_pl": "schrijven"},
         "past":    {"ik": "schreef", "jij": "schreef", "u": "schreef", "hij": "schreef", "zij": "schreef", "het": "schreef",
                     "wij": "schreven", "jullie": "schreven", "zij_pl": "schreven"},
         "perfect": {"ik": "heb geschreven"},
     }},
    {"infinitive": "lezen",     "english": "to read",  "type": "irregular", "cefr": "A1", "emoji": "📖", "example": "Zij leest een boek.",
     "irregular": {
         "present": {"ik": "lees", "jij": "leest", "u": "leest", "hij": "leest", "zij": "leest", "het": "leest",
                     "wij": "lezen", "jullie": "lezen", "zij_pl": "lezen"},
         "past":    {"ik": "las", "jij": "las", "u": "las", "hij": "las", "zij": "las", "het": "las",
                     "wij": "lazen", "jullie": "lazen", "zij_pl": "lazen"},
         "perfect": {"ik": "heb gelezen"},
     }},
    {"infinitive": "lopen",     "english": "to walk",  "type": "irregular", "cefr": "A1", "emoji": "🚶", "example": "Ik loop naar de winkel.",
     "irregular": {
         "present": {"ik": "loop", "jij": "loopt", "u": "loopt", "hij": "loopt", "zij": "loopt", "het": "loopt",
                     "wij": "lopen", "jullie": "lopen", "zij_pl": "lopen"},
         "past":    {"ik": "liep", "jij": "liep", "u": "liep", "hij": "liep", "zij": "liep", "het": "liep",
                     "wij": "liepen", "jullie": "liepen", "zij_pl": "liepen"},
         "perfect": {"ik": "heb gelopen"},
     }},
    {"infinitive": "vinden",    "english": "to find",  "type": "irregular", "cefr": "A2", "emoji": "🔍", "example": "Ik vind het moeilijk.",
     "irregular": {
         "present": {"ik": "vind", "jij": "vindt", "u": "vindt", "hij": "vindt", "zij": "vindt", "het": "vindt",
                     "wij": "vinden", "jullie": "vinden", "zij_pl": "vinden"},
         "past":    {"ik": "vond", "jij": "vond", "u": "vond", "hij": "vond", "zij": "vond", "het": "vond",
                     "wij": "vonden", "jullie": "vonden", "zij_pl": "vonden"},
         "perfect": {"ik": "heb gevonden"},
     }},
    {"infinitive": "kopen",     "english": "to buy",   "type": "irregular", "cefr": "A2", "emoji": "🛒", "example": "Ik koop brood bij de bakker.",
     "irregular": {
         "present": {"ik": "koop", "jij": "koopt", "u": "koopt", "hij": "koopt", "zij": "koopt", "het": "koopt",
                     "wij": "kopen", "jullie": "kopen", "zij_pl": "kopen"},
         "past":    {"ik": "kocht", "jij": "kocht", "u": "kocht", "hij": "kocht", "zij": "kocht", "het": "kocht",
                     "wij": "kochten", "jullie": "kochten", "zij_pl": "kochten"},
         "perfect": {"ik": "heb gekocht"},
     }},

    # ── Modal / auxiliary ──────────────────────────────────────────────
    {"infinitive": "kunnen",    "english": "can / to be able to", "type": "modal", "cefr": "A1", "emoji": "💪", "example": "Ik kan Nederlands spreken.",
     "irregular": {
         "present": {"ik": "kan", "jij": "kan/kunt", "u": "kan/kunt", "hij": "kan", "zij": "kan", "het": "kan",
                     "wij": "kunnen", "jullie": "kunnen", "zij_pl": "kunnen"},
         "past":    {"ik": "kon", "jij": "kon", "u": "kon", "hij": "kon", "zij": "kon", "het": "kon",
                     "wij": "konden", "jullie": "konden", "zij_pl": "konden"},
         "perfect": {"ik": "heb gekund"},
     }},
    {"infinitive": "moeten",    "english": "must / to have to", "type": "modal", "cefr": "A1", "emoji": "⚠️", "example": "Ik moet naar school.",
     "irregular": {
         "present": {"ik": "moet", "jij": "moet", "u": "moet", "hij": "moet", "zij": "moet", "het": "moet",
                     "wij": "moeten", "jullie": "moeten", "zij_pl": "moeten"},
         "past":    {"ik": "moest", "jij": "moest", "u": "moest", "hij": "moest", "zij": "moest", "het": "moest",
                     "wij": "moesten", "jullie": "moesten", "zij_pl": "moesten"},
         "perfect": {"ik": "heb gemoeten"},
     }},
    {"infinitive": "willen",    "english": "to want", "type": "modal", "cefr": "A1", "emoji": "🙋", "example": "Ik wil graag een koffie.",
     "irregular": {
         "present": {"ik": "wil", "jij": "wil/wilt", "u": "wil/wilt", "hij": "wil", "zij": "wil", "het": "wil",
                     "wij": "willen", "jullie": "willen", "zij_pl": "willen"},
         "past":    {"ik": "wilde", "jij": "wilde", "u": "wilde", "hij": "wilde", "zij": "wilde", "het": "wilde",
                     "wij": "wilden", "jullie": "wilden", "zij_pl": "wilden"},
         "perfect": {"ik": "heb gewild"},
     }},
]


def conjugate(verb_entry, tense, pronoun):
    """
    Return the conjugated form for a given verb, tense, and pronoun.
    verb_entry is a dict from VERBS.
    Accepts alternatives separated by '/', like "kan/kunt".
    """
    # Check for explicit irregular form
    irr = verb_entry.get("irregular", {})
    if tense in irr and pronoun in irr[tense]:
        return irr[tense][pronoun]

    # Regular fallback
    stem = verb_entry.get("stem", "")
    if tense == "present":
        return _regular_present(stem, pronoun)
    elif tense == "past":
        return _regular_past(stem, pronoun)
    elif tense == "perfect":
        return _regular_perfect(stem, pronoun)

    return "?"


def check_answer(verb_entry, tense, pronoun, user_answer):
    """
    Return (is_correct, correct_form).
    Handles alternate forms like 'kan/kunt' — accepts either variant.
    """
    correct = conjugate(verb_entry, tense, pronoun)
    # Split on '/' for alternatives
    alternatives = [a.strip().lower() for a in correct.split("/")]
    user = user_answer.strip().lower()
    return user in alternatives, correct
