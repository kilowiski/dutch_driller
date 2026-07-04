"""
Dutch verb bank with conjugation rules.
Supports: present, past (imperfectum), and present perfect (perfectum).
"""

PRONOUNS = {
    "ik": "I", "jij": "you (sg inf)", "u": "you (formal)",
    "hij": "he", "zij": "she", "het": "it",
    "wij": "we", "jullie": "you (pl)", "zij_pl": "they",
}

TENSES = ["present", "past", "perfect"]
TENSE_LABEL = {
    "present": "present tense (tegenwoordige tijd)",
    "past":    "simple past (onvoltooid verleden tijd)",
    "perfect": "present perfect (voltooid tegenwoordige tijd)",
}

def _reg_present(stem, pronoun):
    if pronoun == "ik": return stem
    if pronoun in ("jij","u","hij","zij","het"): return stem + "t"
    return stem

def _reg_past(stem, pronoun):
    soft = set("tkfschp"); suffix = stem[-1] in soft if stem else False
    sg = "te" if suffix else "de"; pl = "ten" if suffix else "den"
    return stem + sg if pronoun in ("ik","jij","u","hij","zij","het") else stem + pl

def _reg_perfect(stem):
    soft = set("tkfschp"); suffix = "t" if (stem[-1] in soft if stem else False) else "d"
    return "ge" + stem + suffix

VERBS = [
    # Regular
    {"infinitive": "werken",    "translation": "to work",   "type": "regular", "stem": "werk",   "cefr": "A1", "example": "Ik werk vijf dagen per week."},
    {"infinitive": "wonen",     "translation": "to live",   "type": "regular", "stem": "woon",   "cefr": "A1", "example": "Wij wonen in een klein dorp."},
    {"infinitive": "leren",     "translation": "to learn",  "type": "regular", "stem": "leer",   "cefr": "A1", "example": "Zij leert Nederlands op school."},
    {"infinitive": "spelen",    "translation": "to play",   "type": "regular", "stem": "speel",  "cefr": "A1", "example": "De kinderen spelen in de tuin."},
    {"infinitive": "koken",     "translation": "to cook",   "type": "regular", "stem": "kook",   "cefr": "A1", "example": "Mijn moeder kookt graag."},
    {"infinitive": "praten",    "translation": "to talk",   "type": "regular", "stem": "praat",  "cefr": "A1", "example": "Zij praten over het weer."},
    {"infinitive": "luisteren", "translation": "to listen", "type": "regular", "stem": "luister","cefr": "A2", "example": "Ik luister naar muziek."},
    {"infinitive": "fietsen",   "translation": "to cycle",  "type": "regular", "stem": "fiets",  "cefr": "A1", "example": "Wij fietsen elke dag naar school."},
    {"infinitive": "reizen",    "translation": "to travel", "type": "regular", "stem": "reis",   "cefr": "A2", "example": "Zij reizen graag naar het buitenland."},
    {"infinitive": "dansen",    "translation": "to dance",  "type": "regular", "stem": "dans",   "cefr": "A2", "example": "Zij dansen de hele nacht."},
    {"infinitive": "maken",     "translation": "to make",   "type": "regular", "stem": "maak",   "cefr": "A1", "example": "Ik maak het ontbijt klaar."},
    {"infinitive": "huren",     "translation": "to rent",   "type": "regular", "stem": "huur",   "cefr": "A2", "example": "Wij huren een appartement in de stad."},
    {"infinitive": "bellen",    "translation": "to call",   "type": "regular", "stem": "bel",    "cefr": "A2", "example": "Ik bel je morgen terug."},
    {"infinitive": "proberen",  "translation": "to try",    "type": "regular", "stem": "probeer","cefr": "A2", "example": "Ik probeer Nederlands te spreken."},
    {"infinitive": "gebruiken", "translation": "to use",    "type": "regular", "stem": "gebruik","cefr": "A2", "example": "Zij gebruikt haar telefoon veel."},

    # Irregular
    {"infinitive": "zijn",      "translation": "to be",   "type": "irregular", "cefr": "A1", "example": "Ik ben moe vandaag.",
     "irregular": {
         "present": {"ik":"ben","jij":"bent","u":"bent","hij":"is","zij":"is","het":"is","wij":"zijn","jullie":"zijn","zij_pl":"zijn"},
         "past":    {"ik":"was","jij":"was","u":"was","hij":"was","zij":"was","het":"was","wij":"waren","jullie":"waren","zij_pl":"waren"},
         "perfect": {"ik":"ben geweest"},
     }},
    {"infinitive": "hebben",    "translation": "to have", "type": "irregular", "cefr": "A1", "example": "Ik heb een vraag.",
     "irregular": {
         "present": {"ik":"heb","jij":"hebt","u":"hebt","hij":"heeft","zij":"heeft","het":"heeft","wij":"hebben","jullie":"hebben","zij_pl":"hebben"},
         "past":    {"ik":"had","jij":"had","u":"had","hij":"had","zij":"had","het":"had","wij":"hadden","jullie":"hadden","zij_pl":"hadden"},
         "perfect": {"ik":"heb gehad"},
     }},
    {"infinitive": "gaan",      "translation": "to go",   "type": "irregular", "cefr": "A1", "example": "Ik ga naar huis.",
     "irregular": {
         "present": {"ik":"ga","jij":"gaat","u":"gaat","hij":"gaat","zij":"gaat","het":"gaat","wij":"gaan","jullie":"gaan","zij_pl":"gaan"},
         "past":    {"ik":"ging","jij":"ging","u":"ging","hij":"ging","zij":"ging","het":"ging","wij":"gingen","jullie":"gingen","zij_pl":"gingen"},
         "perfect": {"ik":"is gegaan"},
     }},
    {"infinitive": "komen",     "translation": "to come",  "type": "irregular", "cefr": "A1", "example": "Zij komt uit Nederland.",
     "irregular": {
         "present": {"ik":"kom","jij":"komt","u":"komt","hij":"komt","zij":"komt","het":"komt","wij":"komen","jullie":"komen","zij_pl":"komen"},
         "past":    {"ik":"kwam","jij":"kwam","u":"kwam","hij":"kwam","zij":"kwam","het":"kwam","wij":"kwamen","jullie":"kwamen","zij_pl":"kwamen"},
         "perfect": {"ik":"is gekomen"},
     }},
    {"infinitive": "doen",      "translation": "to do",    "type": "irregular", "cefr": "A1", "example": "Wat doe je vandaag?",
     "irregular": {
         "present": {"ik":"doe","jij":"doet","u":"doet","hij":"doet","zij":"doet","het":"doet","wij":"doen","jullie":"doen","zij_pl":"doen"},
         "past":    {"ik":"deed","jij":"deed","u":"deed","hij":"deed","zij":"deed","het":"deed","wij":"deden","jullie":"deden","zij_pl":"deden"},
         "perfect": {"ik":"heb gedaan"},
     }},
    {"infinitive": "zien",      "translation": "to see",   "type": "irregular", "cefr": "A1", "example": "Ik zie een vogel in de boom.",
     "irregular": {
         "present": {"ik":"zie","jij":"ziet","u":"ziet","hij":"ziet","zij":"ziet","het":"ziet","wij":"zien","jullie":"zien","zij_pl":"zien"},
         "past":    {"ik":"zag","jij":"zag","u":"zag","hij":"zag","zij":"zag","het":"zag","wij":"zagen","jullie":"zagen","zij_pl":"zagen"},
         "perfect": {"ik":"heb gezien"},
     }},
    {"infinitive": "eten",      "translation": "to eat",   "type": "irregular", "cefr": "A1", "example": "Wij eten om zes uur.",
     "irregular": {
         "present": {"ik":"eet","jij":"eet","u":"eet","hij":"eet","zij":"eet","het":"eet","wij":"eten","jullie":"eten","zij_pl":"eten"},
         "past":    {"ik":"at","jij":"at","u":"at","hij":"at","zij":"at","het":"at","wij":"aten","jullie":"aten","zij_pl":"aten"},
         "perfect": {"ik":"heb gegeten"},
     }},
    {"infinitive": "drinken",   "translation": "to drink", "type": "irregular", "cefr": "A1", "example": "Ik drink koffie in de ochtend.",
     "irregular": {
         "present": {"ik":"drink","jij":"drinkt","u":"drinkt","hij":"drinkt","zij":"drinkt","het":"drinkt","wij":"drinken","jullie":"drinken","zij_pl":"drinken"},
         "past":    {"ik":"dronk","jij":"dronk","u":"dronk","hij":"dronk","zij":"dronk","het":"dronk","wij":"dronken","jullie":"dronken","zij_pl":"dronken"},
         "perfect": {"ik":"heb gedronken"},
     }},
    {"infinitive": "spreken",   "translation": "to speak", "type": "irregular", "cefr": "A1", "example": "Spreekt u Nederlands?",
     "irregular": {
         "present": {"ik":"spreek","jij":"spreekt","u":"spreekt","hij":"spreekt","zij":"spreekt","het":"spreekt","wij":"spreken","jullie":"spreken","zij_pl":"spreken"},
         "past":    {"ik":"sprak","jij":"sprak","u":"sprak","hij":"sprak","zij":"sprak","het":"sprak","wij":"spraken","jullie":"spraken","zij_pl":"spraken"},
         "perfect": {"ik":"heb gesproken"},
     }},
    {"infinitive": "schrijven", "translation": "to write", "type": "irregular", "cefr": "A1", "example": "Ik schrijf een brief.",
     "irregular": {
         "present": {"ik":"schrijf","jij":"schrijft","u":"schrijft","hij":"schrijft","zij":"schrijft","het":"schrijft","wij":"schrijven","jullie":"schrijven","zij_pl":"schrijven"},
         "past":    {"ik":"schreef","jij":"schreef","u":"schreef","hij":"schreef","zij":"schreef","het":"schreef","wij":"schreven","jullie":"schreven","zij_pl":"schreven"},
         "perfect": {"ik":"heb geschreven"},
     }},
    {"infinitive": "lezen",     "translation": "to read",  "type": "irregular", "cefr": "A1", "example": "Zij leest een boek.",
     "irregular": {
         "present": {"ik":"lees","jij":"leest","u":"leest","hij":"leest","zij":"leest","het":"leest","wij":"lezen","jullie":"lezen","zij_pl":"lezen"},
         "past":    {"ik":"las","jij":"las","u":"las","hij":"las","zij":"las","het":"las","wij":"lazen","jullie":"lazen","zij_pl":"lazen"},
         "perfect": {"ik":"heb gelezen"},
     }},
    {"infinitive": "lopen",     "translation": "to walk",  "type": "irregular", "cefr": "A1", "example": "Ik loop naar de winkel.",
     "irregular": {
         "present": {"ik":"loop","jij":"loopt","u":"loopt","hij":"loopt","zij":"loopt","het":"loopt","wij":"lopen","jullie":"lopen","zij_pl":"lopen"},
         "past":    {"ik":"liep","jij":"liep","u":"liep","hij":"liep","zij":"liep","het":"liep","wij":"liepen","jullie":"liepen","zij_pl":"liepen"},
         "perfect": {"ik":"heb gelopen"},
     }},

    # Modals
    {"infinitive": "kunnen",    "translation": "can / to be able to", "type": "modal", "cefr": "A1", "example": "Ik kan Nederlands spreken.",
     "irregular": {
         "present": {"ik":"kan","jij":"kan/kunt","u":"kan/kunt","hij":"kan","zij":"kan","het":"kan","wij":"kunnen","jullie":"kunnen","zij_pl":"kunnen"},
         "past":    {"ik":"kon","jij":"kon","u":"kon","hij":"kon","zij":"kon","het":"kon","wij":"konden","jullie":"konden","zij_pl":"konden"},
         "perfect": {"ik":"heb gekund"},
     }},
    {"infinitive": "moeten",    "translation": "must / to have to", "type": "modal", "cefr": "A1", "example": "Ik moet naar school.",
     "irregular": {
         "present": {"ik":"moet","jij":"moet","u":"moet","hij":"moet","zij":"moet","het":"moet","wij":"moeten","jullie":"moeten","zij_pl":"moeten"},
         "past":    {"ik":"moest","jij":"moest","u":"moest","hij":"moest","zij":"moest","het":"moest","wij":"moesten","jullie":"moesten","zij_pl":"moesten"},
         "perfect": {"ik":"heb gemoeten"},
     }},
    {"infinitive": "willen",    "translation": "to want", "type": "modal", "cefr": "A1", "example": "Ik wil graag een koffie.",
     "irregular": {
         "present": {"ik":"wil","jij":"wil/wilt","u":"wil/wilt","hij":"wil","zij":"wil","het":"wil","wij":"willen","jullie":"willen","zij_pl":"willen"},
         "past":    {"ik":"wilde","jij":"wilde","u":"wilde","hij":"wilde","zij":"wilde","het":"wilde","wij":"wilden","jullie":"wilden","zij_pl":"wilden"},
         "perfect": {"ik":"heb gewild"},
     }},
]

def conjugate(verb_entry, tense, pronoun):
    irr = verb_entry.get("irregular", {})
    if tense in irr and pronoun in irr[tense]:
        return irr[tense][pronoun]
    stem = verb_entry.get("stem", "")
    if tense == "present": return _reg_present(stem, pronoun)
    if tense == "past":    return _reg_past(stem, pronoun)
    if tense == "perfect": return _reg_perfect(stem)
    return "?"

def check_answer(verb_entry, tense, pronoun, user_answer):
    correct = conjugate(verb_entry, tense, pronoun)
    alts = [a.strip().lower() for a in correct.split("/")]
    return user_answer.strip().lower() in alts, correct
