"""
Dutch vocabulary bank organized by theme.
Each entry: (dutch, english, category)
"""

VOCABULARY = [
    # ── Basics / Greetings ──────────────────────────────────────────
    ("hallo",       "hello",        "basics"),
    ("tot ziens",   "goodbye",      "basics"),
    ("alsjeblieft", "please",       "basics"),
    ("dank je wel", "thank you",    "basics"),
    ("ja",          "yes",          "basics"),
    ("nee",         "no",           "basics"),
    ("misschien",   "maybe",        "basics"),
    ("goedemorgen", "good morning", "basics"),
    ("goedenavond", "good evening", "basics"),
    ("welterusten", "good night",   "basics"),

    # ── People & Family ─────────────────────────────────────────────
    ("de man",      "the man",      "people"),
    ("de vrouw",    "the woman",    "people"),
    ("het kind",    "the child",    "people"),
    ("de vriend",   "the friend (m)", "people"),
    ("de vriendin", "the friend (f)", "people"),
    ("de vader",    "the father",   "people"),
    ("de moeder",   "the mother",   "people"),
    ("de broer",    "the brother",  "people"),
    ("de zus",      "the sister",   "people"),
    ("de zoon",     "the son",      "people"),
    ("de dochter",  "the daughter", "people"),
    ("de familie",  "the family",   "people"),

    # ── Food & Drink ────────────────────────────────────────────────
    ("het water",   "the water",    "food"),
    ("het brood",   "the bread",    "food"),
    ("de kaas",     "the cheese",   "food"),
    ("de melk",     "the milk",     "food"),
    ("het bier",    "the beer",     "food"),
    ("de koffie",   "the coffee",   "food"),
    ("de thee",     "the tea",      "food"),
    ("de wijn",     "the wine",     "food"),
    ("het vlees",   "the meat",     "food"),
    ("de vis",      "the fish",     "food"),
    ("de groente",  "the vegetable","food"),
    ("het fruit",   "the fruit",    "food"),
    ("het ei",      "the egg",      "food"),
    ("de suiker",   "the sugar",    "food"),
    ("het zout",    "the salt",     "food"),

    # ── Home & Objects ──────────────────────────────────────────────
    ("het huis",    "the house",    "home"),
    ("de kamer",    "the room",     "home"),
    ("de deur",     "the door",     "home"),
    ("het raam",    "the window",   "home"),
    ("de tafel",    "the table",    "home"),
    ("de stoel",    "the chair",    "home"),
    ("het bed",     "the bed",      "home"),
    ("de keuken",   "the kitchen",  "home"),
    ("de badkamer", "the bathroom", "home"),
    ("de sleutel",  "the key",      "home"),

    # ── Transport & Places ──────────────────────────────────────────
    ("de auto",     "the car",      "transport"),
    ("de fiets",    "the bicycle",  "transport"),
    ("de trein",    "the train",    "transport"),
    ("het station", "the station",  "transport"),
    ("de straat",   "the street",   "transport"),
    ("de stad",     "the city",     "transport"),
    ("het dorp",    "the village",  "transport"),
    ("de winkel",   "the shop",     "transport"),
    ("het vliegveld","the airport", "transport"),

    # ── Time & Weather ──────────────────────────────────────────────
    ("vandaag",     "today",        "time"),
    ("morgen",      "tomorrow",     "time"),
    ("gisteren",    "yesterday",    "time"),
    ("nu",          "now",          "time"),
    ("later",       "later",        "time"),
    ("vroeg",       "early",        "time"),
    ("laat",        "late",         "time"),
    ("de dag",      "the day",      "time"),
    ("de nacht",    "the night",    "time"),
    ("de week",     "the week",     "time"),
    ("het weer",    "the weather",  "time"),
    ("de zon",      "the sun",      "time"),
    ("de regen",    "the rain",     "time"),
    ("koud",        "cold",         "time"),
    ("warm",        "warm",         "time"),

    # ── Common Adjectives ───────────────────────────────────────────
    ("groot",       "big",          "adjectives"),
    ("klein",       "small",        "adjectives"),
    ("goed",        "good",         "adjectives"),
    ("slecht",      "bad",          "adjectives"),
    ("mooi",        "beautiful",    "adjectives"),
    ("lelijk",      "ugly",         "adjectives"),
    ("oud",         "old",          "adjectives"),
    ("nieuw",       "new",          "adjectives"),
    ("lang",        "long / tall",  "adjectives"),
    ("kort",        "short",        "adjectives"),
    ("snel",        "fast",         "adjectives"),
    ("langzaam",    "slow",         "adjectives"),
    ("duur",        "expensive",    "adjectives"),
    ("goedkoop",    "cheap",        "adjectives"),
    ("makkelijk",   "easy",         "adjectives"),
    ("moeilijk",    "difficult",    "adjectives"),
    ("belangrijk",  "important",    "adjectives"),

    # ── Numbers ─────────────────────────────────────────────────────
    ("een",         "one",          "numbers"),
    ("twee",        "two",          "numbers"),
    ("drie",        "three",        "numbers"),
    ("vier",        "four",         "numbers"),
    ("vijf",        "five",         "numbers"),
    ("zes",         "six",          "numbers"),
    ("zeven",       "seven",        "numbers"),
    ("acht",        "eight",        "numbers"),
    ("negen",       "nine",         "numbers"),
    ("tien",        "ten",          "numbers"),
    ("twintig",     "twenty",       "numbers"),
    ("honderd",     "hundred",      "numbers"),

    # ── Colors ──────────────────────────────────────────────────────
    ("rood",        "red",          "colors"),
    ("blauw",       "blue",         "colors"),
    ("groen",       "green",        "colors"),
    ("geel",        "yellow",       "colors"),
    ("zwart",       "black",        "colors"),
    ("wit",         "white",        "colors"),
    ("oranje",      "orange",       "colors"),
    ("paars",       "purple",       "colors"),

    # ── Phrases / Survival ──────────────────────────────────────────
    ("hoe gaat het?",   "how are you?",     "phrases"),
    ("ik begrijp het niet", "I don't understand", "phrases"),
    ("ik spreek een beetje Nederlands", "I speak a little Dutch", "phrases"),
    ("spreekt u Engels?",   "do you speak English?", "phrases"),
    ("waar is het toilet?", "where is the toilet?",  "phrases"),
    ("hoeveel kost dit?",   "how much does this cost?", "phrases"),
    ("ik wil graag...",     "I would like...",    "phrases"),
]

CATEGORIES = sorted(set(cat for _, _, cat in VOCABULARY))

# Build lookup index: {category: [items]}
BY_CATEGORY = {}
for item in VOCABULARY:
    cat = item[2]
    BY_CATEGORY.setdefault(cat, []).append(item)
