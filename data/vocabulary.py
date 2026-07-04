"""
Dutch vocabulary bank organized by theme.
Each entry is a dict: dutch, english, category, cefr, example.
"""

VOCABULARY = [
    # ── Basics / Greetings ──────────────────────────────────────────
    {"dutch": "hallo",       "english": "hello",         "category": "basics",   "cefr": "A1", "example": "Hallo, hoe gaat het?"},
    {"dutch": "tot ziens",   "english": "goodbye",       "category": "basics",   "cefr": "A1", "example": "Tot ziens en tot morgen!"},
    {"dutch": "alsjeblieft", "english": "please",        "category": "basics",   "cefr": "A1", "example": "Een koffie, alsjeblieft."},
    {"dutch": "dank je wel", "english": "thank you",     "category": "basics",   "cefr": "A1", "example": "Dank je wel voor het eten."},
    {"dutch": "ja",          "english": "yes",           "category": "basics",   "cefr": "A1", "example": "Ja, ik wil graag een biertje."},
    {"dutch": "nee",         "english": "no",            "category": "basics",   "cefr": "A1", "example": "Nee, dank je. Ik heb geen honger."},
    {"dutch": "misschien",   "english": "maybe",         "category": "basics",   "cefr": "A1", "example": "Misschien gaan we morgen naar het strand."},
    {"dutch": "goedemorgen", "english": "good morning",  "category": "basics",   "cefr": "A1", "example": "Goedemorgen, heb je lekker geslapen?"},
    {"dutch": "goedenavond", "english": "good evening",  "category": "basics",   "cefr": "A1", "example": "Goedenavond, een tafel voor twee graag."},
    {"dutch": "welterusten", "english": "good night",    "category": "basics",   "cefr": "A1", "example": "Welterusten, slaap lekker!"},

    # ── People & Family ─────────────────────────────────────────────
    {"dutch": "de man",      "english": "the man",       "category": "people",   "cefr": "A1", "example": "De man leest de krant."},
    {"dutch": "de vrouw",    "english": "the woman",     "category": "people",   "cefr": "A1", "example": "De vrouw drinkt koffie."},
    {"dutch": "het kind",    "english": "the child",     "category": "people",   "cefr": "A1", "example": "Het kind speelt in de tuin."},
    {"dutch": "de vriend",   "english": "the friend (m)","category": "people",   "cefr": "A1", "example": "Mijn vriend woont in Amsterdam."},
    {"dutch": "de vriendin", "english": "the friend (f)","category": "people",   "cefr": "A1", "example": "Mijn vriendin studeert Nederlands."},
    {"dutch": "de vader",    "english": "the father",    "category": "people",   "cefr": "A1", "example": "Mijn vader werkt in het ziekenhuis."},
    {"dutch": "de moeder",   "english": "the mother",    "category": "people",   "cefr": "A1", "example": "Mijn moeder kookt graag."},
    {"dutch": "de broer",    "english": "the brother",   "category": "people",   "cefr": "A1", "example": "Mijn broer is ouder dan ik."},
    {"dutch": "de zus",      "english": "the sister",    "category": "people",   "cefr": "A1", "example": "Mijn zus speelt gitaar."},
    {"dutch": "de zoon",     "english": "the son",       "category": "people",   "cefr": "A1", "example": "Haar zoon gaat naar school."},
    {"dutch": "de dochter",  "english": "the daughter",  "category": "people",   "cefr": "A1", "example": "Zijn dochter is tien jaar oud."},
    {"dutch": "de familie",  "english": "the family",    "category": "people",   "cefr": "A1", "example": "De familie komt op bezoek."},

    # ── Food & Drink ────────────────────────────────────────────────
    {"dutch": "het water",   "english": "the water",     "category": "food",     "cefr": "A1", "example": "Mag ik een glas water?"},
    {"dutch": "het brood",   "english": "the bread",     "category": "food",     "cefr": "A1", "example": "Ik koop brood bij de bakker."},
    {"dutch": "de kaas",     "english": "the cheese",    "category": "food",     "cefr": "A1", "example": "Nederlandse kaas is erg lekker."},
    {"dutch": "de melk",     "english": "the milk",      "category": "food",     "cefr": "A1", "example": "Ik drink elke ochtend melk."},
    {"dutch": "het bier",    "english": "the beer",      "category": "food",     "cefr": "A1", "example": "Een koud biertje, graag."},
    {"dutch": "de koffie",   "english": "the coffee",    "category": "food",     "cefr": "A1", "example": "Zwarte koffie zonder suiker."},
    {"dutch": "de thee",     "english": "the tea",       "category": "food",     "cefr": "A1", "example": "Wil je een kopje thee?"},
    {"dutch": "de wijn",     "english": "the wine",      "category": "food",     "cefr": "A2", "example": "Rode wijn past goed bij het vlees."},
    {"dutch": "het vlees",   "english": "the meat",      "category": "food",     "cefr": "A2", "example": "Eet je vlees of ben je vegetarier?"},
    {"dutch": "de vis",      "english": "the fish",      "category": "food",     "cefr": "A1", "example": "We eten vanavond vis."},
    {"dutch": "de groente",  "english": "the vegetable", "category": "food",     "cefr": "A2", "example": "Eet je groente, dat is gezond."},
    {"dutch": "het fruit",   "english": "the fruit",     "category": "food",     "cefr": "A1", "example": "Ik eet elke dag fruit."},
    {"dutch": "het ei",      "english": "the egg",       "category": "food",     "cefr": "A1", "example": "Twee eieren voor het ontbijt."},
    {"dutch": "de suiker",   "english": "the sugar",     "category": "food",     "cefr": "A1", "example": "Doe je suiker in de koffie?"},
    {"dutch": "het zout",    "english": "the salt",      "category": "food",     "cefr": "A1", "example": "Een beetje zout in de soep."},

    # ── Home & Objects ──────────────────────────────────────────────
    {"dutch": "het huis",    "english": "the house",      "category": "home",    "cefr": "A1", "example": "Ons huis heeft drie kamers."},
    {"dutch": "de kamer",    "english": "the room",       "category": "home",    "cefr": "A1", "example": "Mijn kamer is niet zo groot."},
    {"dutch": "de deur",     "english": "the door",       "category": "home",    "cefr": "A1", "example": "Doe de deur dicht, het is koud."},
    {"dutch": "het raam",    "english": "the window",     "category": "home",    "cefr": "A1", "example": "Het raam staat open."},
    {"dutch": "de tafel",    "english": "the table",      "category": "home",    "cefr": "A1", "example": "De sleutels liggen op de tafel."},
    {"dutch": "de stoel",    "english": "the chair",      "category": "home",    "cefr": "A1", "example": "Ga zitten op de stoel."},
    {"dutch": "het bed",     "english": "the bed",        "category": "home",    "cefr": "A1", "example": "Ik ga om tien uur naar bed."},
    {"dutch": "de keuken",   "english": "the kitchen",    "category": "home",    "cefr": "A1", "example": "We koken samen in de keuken."},
    {"dutch": "de badkamer", "english": "the bathroom",   "category": "home",    "cefr": "A1", "example": "De badkamer is op de eerste verdieping."},
    {"dutch": "de sleutel",  "english": "the key",        "category": "home",    "cefr": "A1", "example": "Ik ben mijn sleutel kwijt."},

    # ── Transport & Places ──────────────────────────────────────────
    {"dutch": "de auto",     "english": "the car",        "category": "transport","cefr": "A1", "example": "De auto staat voor het huis."},
    {"dutch": "de fiets",    "english": "the bicycle",    "category": "transport","cefr": "A1", "example": "In Nederland fietst iedereen."},
    {"dutch": "de trein",    "english": "the train",      "category": "transport","cefr": "A1", "example": "De trein naar Utrecht vertrekt om drie uur."},
    {"dutch": "het station", "english": "the station",    "category": "transport","cefr": "A2", "example": "We spreken af op het station."},
    {"dutch": "de straat",   "english": "the street",     "category": "transport","cefr": "A1", "example": "Kinderen spelen op straat."},
    {"dutch": "de stad",     "english": "the city",       "category": "transport","cefr": "A1", "example": "Amsterdam is een mooie stad."},
    {"dutch": "het dorp",    "english": "the village",    "category": "transport","cefr": "A2", "example": "Zij woont in een klein dorp."},
    {"dutch": "de winkel",   "english": "the shop",       "category": "transport","cefr": "A1", "example": "De winkel gaat om negen uur open."},
    {"dutch": "het vliegveld","english": "the airport",   "category": "transport","cefr": "A2", "example": "Het vliegveld is ver van de stad."},

    # ── Time & Weather ──────────────────────────────────────────────
    {"dutch": "vandaag",     "english": "today",          "category": "time",     "cefr": "A1", "example": "Vandaag is het maandag."},
    {"dutch": "morgen",      "english": "tomorrow",       "category": "time",     "cefr": "A1", "example": "Morgen ga ik naar de dokter."},
    {"dutch": "gisteren",    "english": "yesterday",      "category": "time",     "cefr": "A1", "example": "Gisteren was het lekker weer."},
    {"dutch": "nu",          "english": "now",            "category": "time",     "cefr": "A1", "example": "Wat doe je nu?"},
    {"dutch": "later",       "english": "later",          "category": "time",     "cefr": "A1", "example": "Ik bel je later terug."},
    {"dutch": "vroeg",       "english": "early",          "category": "time",     "cefr": "A2", "example": "Ik sta vroeg op om te sporten."},
    {"dutch": "laat",        "english": "late",           "category": "time",     "cefr": "A1", "example": "Het is laat, ik ga naar bed."},
    {"dutch": "de dag",      "english": "the day",        "category": "time",     "cefr": "A1", "example": "Fijne dag nog!"},
    {"dutch": "de nacht",    "english": "the night",      "category": "time",     "cefr": "A1", "example": "Het was een lange nacht."},
    {"dutch": "de week",     "english": "the week",       "category": "time",     "cefr": "A1", "example": "Deze week heb ik vrij."},
    {"dutch": "het weer",    "english": "the weather",    "category": "time",     "cefr": "A2", "example": "Het weer is slecht vandaag."},
    {"dutch": "de zon",      "english": "the sun",        "category": "time",     "cefr": "A1", "example": "De zon schijnt vandaag."},
    {"dutch": "de regen",    "english": "the rain",       "category": "time",     "cefr": "A1", "example": "De regen komt met bakken uit de lucht."},
    {"dutch": "koud",        "english": "cold",           "category": "time",     "cefr": "A1", "example": "Het is koud buiten, draag een jas."},
    {"dutch": "warm",        "english": "warm",           "category": "time",     "cefr": "A1", "example": "Het is warm vandaag, laten we gaan zwemmen."},

    # ── Common Adjectives ───────────────────────────────────────────
    {"dutch": "groot",       "english": "big",            "category": "adjectives","cefr": "A1", "example": "Amsterdam is een grote stad."},
    {"dutch": "klein",       "english": "small",          "category": "adjectives","cefr": "A1", "example": "Een klein kopje koffie graag."},
    {"dutch": "goed",        "english": "good",           "category": "adjectives","cefr": "A1", "example": "Het eten is erg goed hier."},
    {"dutch": "slecht",      "english": "bad",            "category": "adjectives","cefr": "A1", "example": "Het weer is slecht vandaag."},
    {"dutch": "mooi",        "english": "beautiful",      "category": "adjectives","cefr": "A1", "example": "Wat een mooie jurk!"},
    {"dutch": "lelijk",      "english": "ugly",           "category": "adjectives","cefr": "A2", "example": "Dat gebouw is echt lelijk."},
    {"dutch": "oud",         "english": "old",            "category": "adjectives","cefr": "A1", "example": "Dit huis is heel oud."},
    {"dutch": "nieuw",       "english": "new",            "category": "adjectives","cefr": "A1", "example": "Ik heb een nieuwe auto gekocht."},
    {"dutch": "lang",        "english": "long / tall",    "category": "adjectives","cefr": "A1", "example": "Mijn broer is erg lang."},
    {"dutch": "kort",        "english": "short",          "category": "adjectives","cefr": "A1", "example": "Het is een kort verhaal."},
    {"dutch": "snel",        "english": "fast",           "category": "adjectives","cefr": "A1", "example": "De trein is heel snel."},
    {"dutch": "langzaam",    "english": "slow",           "category": "adjectives","cefr": "A2", "example": "De bus is erg langzaam."},
    {"dutch": "duur",        "english": "expensive",      "category": "adjectives","cefr": "A2", "example": "Deze wijn is te duur."},
    {"dutch": "goedkoop",    "english": "cheap",          "category": "adjectives","cefr": "A2", "example": "De groente is goedkoop op de markt."},
    {"dutch": "makkelijk",   "english": "easy",           "category": "adjectives","cefr": "A2", "example": "Nederlands is niet makkelijk!"},
    {"dutch": "moeilijk",    "english": "difficult",      "category": "adjectives","cefr": "A2", "example": "Deze vraag is moeilijk."},
    {"dutch": "belangrijk",  "english": "important",      "category": "adjectives","cefr": "A2", "example": "Dit is een belangrijke afspraak."},

    # ── Numbers ─────────────────────────────────────────────────────
    {"dutch": "een",         "english": "one",            "category": "numbers",  "cefr": "A1", "example": "Ik heb een broer."},
    {"dutch": "twee",        "english": "two",            "category": "numbers",  "cefr": "A1", "example": "Twee koffie, alsjeblieft."},
    {"dutch": "drie",        "english": "three",          "category": "numbers",  "cefr": "A1", "example": "Drie keer per week sport ik."},
    {"dutch": "vier",        "english": "four",           "category": "numbers",  "cefr": "A1", "example": "Het feest begint om vier uur."},
    {"dutch": "vijf",        "english": "five",           "category": "numbers",  "cefr": "A1", "example": "Ik heb vijf minuten nodig."},
    {"dutch": "zes",         "english": "six",            "category": "numbers",  "cefr": "A1", "example": "Zes eieren voor de cake."},
    {"dutch": "zeven",       "english": "seven",          "category": "numbers",  "cefr": "A1", "example": "De winkel is open tot zeven uur."},
    {"dutch": "acht",        "english": "eight",          "category": "numbers",  "cefr": "A1", "example": "Mijn zoon is acht jaar."},
    {"dutch": "negen",       "english": "nine",           "category": "numbers",  "cefr": "A1", "example": "Het is negen uur 's ochtends."},
    {"dutch": "tien",        "english": "ten",            "category": "numbers",  "cefr": "A1", "example": "Een tien voor je examen!"},
    {"dutch": "twintig",     "english": "twenty",         "category": "numbers",  "cefr": "A1", "example": "Het kost twintig euro."},
    {"dutch": "honderd",     "english": "hundred",        "category": "numbers",  "cefr": "A1", "example": "Honderd procent zeker!"},

    # ── Colors ──────────────────────────────────────────────────────
    {"dutch": "rood",        "english": "red",            "category": "colors",   "cefr": "A1", "example": "De roos is rood."},
    {"dutch": "blauw",       "english": "blue",           "category": "colors",   "cefr": "A1", "example": "De lucht is blauw."},
    {"dutch": "groen",       "english": "green",          "category": "colors",   "cefr": "A1", "example": "Het gras is groen."},
    {"dutch": "geel",        "english": "yellow",         "category": "colors",   "cefr": "A1", "example": "De zon is geel."},
    {"dutch": "zwart",       "english": "black",          "category": "colors",   "cefr": "A1", "example": "De kat is zwart."},
    {"dutch": "wit",         "english": "white",          "category": "colors",   "cefr": "A1", "example": "De muur is wit."},
    {"dutch": "oranje",      "english": "orange",         "category": "colors",   "cefr": "A1", "example": "Oranje is de kleur van Nederland."},
    {"dutch": "paars",       "english": "purple",         "category": "colors",   "cefr": "A2", "example": "Zij draagt een paarse jurk."},

    # ── Phrases / Survival ──────────────────────────────────────────
    {"dutch": "hoe gaat het?",           "english": "how are you?",              "category": "phrases",  "cefr": "A1", "example": "Hoi, hoe gaat het met je?"},
    {"dutch": "ik begrijp het niet",      "english": "I don't understand",        "category": "phrases",  "cefr": "A1", "example": "Sorry, ik begrijp het niet. Kun je dat herhalen?"},
    {"dutch": "ik spreek een beetje Nederlands","english": "I speak a little Dutch","category": "phrases","cefr": "A1", "example": "Ik spreek een beetje Nederlands, maar niet vloeiend."},
    {"dutch": "spreekt u Engels?",       "english": "do you speak English?",      "category": "phrases",  "cefr": "A1", "example": "Sorry, spreekt u Engels?"},
    {"dutch": "waar is het toilet?",     "english": "where is the toilet?",       "category": "phrases",  "cefr": "A1", "example": "Pardon, waar is het toilet?"},
    {"dutch": "hoeveel kost dit?",       "english": "how much does this cost?",   "category": "phrases",  "cefr": "A2", "example": "Hoeveel kost dit boek?"},
    {"dutch": "ik wil graag...",         "english": "I would like...",            "category": "phrases",  "cefr": "A1", "example": "Ik wil graag een cappuccino."},
]

CATEGORIES = sorted(set(e["category"] for e in VOCABULARY))
BY_CATEGORY = {}
for entry in VOCABULARY:
    cat = entry["category"]
    BY_CATEGORY.setdefault(cat, []).append(entry)
