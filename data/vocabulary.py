"""
Dutch vocabulary bank organized by theme.
Each entry is a dict: dutch, english, category, cefr, example.
"""

VOCABULARY = [
    # ── Basics / Greetings ──────────────────────────────────────────
    {"word": "hallo",       "translation": "hello",         "category": "basics",   "cefr": "A1", "example": "Hallo, hoe gaat het?"},
    {"word": "tot ziens",   "translation": "goodbye",       "category": "basics",   "cefr": "A1", "example": "Tot ziens en tot morgen!"},
    {"word": "alsjeblieft", "translation": "please",        "category": "basics",   "cefr": "A1", "example": "Een koffie, alsjeblieft."},
    {"word": "dank je wel", "translation": "thank you",     "category": "basics",   "cefr": "A1", "example": "Dank je wel voor het eten."},
    {"word": "ja",          "translation": "yes",           "category": "basics",   "cefr": "A1", "example": "Ja, ik wil graag een biertje."},
    {"word": "nee",         "translation": "no",            "category": "basics",   "cefr": "A1", "example": "Nee, dank je. Ik heb geen honger."},
    {"word": "misschien",   "translation": "maybe",         "category": "basics",   "cefr": "A1", "example": "Misschien gaan we morgen naar het strand."},
    {"word": "goedemorgen", "translation": "good morning",  "category": "basics",   "cefr": "A1", "example": "Goedemorgen, heb je lekker geslapen?"},
    {"word": "goedenavond", "translation": "good evening",  "category": "basics",   "cefr": "A1", "example": "Goedenavond, een tafel voor twee graag."},
    {"word": "welterusten", "translation": "good night",    "category": "basics",   "cefr": "A1", "example": "Welterusten, slaap lekker!"},

    # ── People & Family ─────────────────────────────────────────────
    {"word": "de man",      "translation": "the man",       "category": "people",   "cefr": "A1", "example": "De man leest de krant."},
    {"word": "de vrouw",    "translation": "the woman",     "category": "people",   "cefr": "A1", "example": "De vrouw drinkt koffie."},
    {"word": "het kind",    "translation": "the child",     "category": "people",   "cefr": "A1", "example": "Het kind speelt in de tuin."},
    {"word": "de vriend",   "translation": "the friend (m)","category": "people",   "cefr": "A1", "example": "Mijn vriend woont in Amsterdam."},
    {"word": "de vriendin", "translation": "the friend (f)","category": "people",   "cefr": "A1", "example": "Mijn vriendin studeert Nederlands."},
    {"word": "de vader",    "translation": "the father",    "category": "people",   "cefr": "A1", "example": "Mijn vader werkt in het ziekenhuis."},
    {"word": "de moeder",   "translation": "the mother",    "category": "people",   "cefr": "A1", "example": "Mijn moeder kookt graag."},
    {"word": "de broer",    "translation": "the brother",   "category": "people",   "cefr": "A1", "example": "Mijn broer is ouder dan ik."},
    {"word": "de zus",      "translation": "the sister",    "category": "people",   "cefr": "A1", "example": "Mijn zus speelt gitaar."},
    {"word": "de zoon",     "translation": "the son",       "category": "people",   "cefr": "A1", "example": "Haar zoon gaat naar school."},
    {"word": "de dochter",  "translation": "the daughter",  "category": "people",   "cefr": "A1", "example": "Zijn dochter is tien jaar oud."},
    {"word": "de familie",  "translation": "the family",    "category": "people",   "cefr": "A1", "example": "De familie komt op bezoek."},

    # ── Food & Drink ────────────────────────────────────────────────
    {"word": "het water",   "translation": "the water",     "category": "food",     "cefr": "A1", "example": "Mag ik een glas water?"},
    {"word": "het brood",   "translation": "the bread",     "category": "food",     "cefr": "A1", "example": "Ik koop brood bij de bakker."},
    {"word": "de kaas",     "translation": "the cheese",    "category": "food",     "cefr": "A1", "example": "Nederlandse kaas is erg lekker."},
    {"word": "de melk",     "translation": "the milk",      "category": "food",     "cefr": "A1", "example": "Ik drink elke ochtend melk."},
    {"word": "het bier",    "translation": "the beer",      "category": "food",     "cefr": "A1", "example": "Een koud biertje, graag."},
    {"word": "de koffie",   "translation": "the coffee",    "category": "food",     "cefr": "A1", "example": "Zwarte koffie zonder suiker."},
    {"word": "de thee",     "translation": "the tea",       "category": "food",     "cefr": "A1", "example": "Wil je een kopje thee?"},
    {"word": "de wijn",     "translation": "the wine",      "category": "food",     "cefr": "A2", "example": "Rode wijn past goed bij het vlees."},
    {"word": "het vlees",   "translation": "the meat",      "category": "food",     "cefr": "A2", "example": "Eet je vlees of ben je vegetarier?"},
    {"word": "de vis",      "translation": "the fish",      "category": "food",     "cefr": "A1", "example": "We eten vanavond vis."},
    {"word": "de groente",  "translation": "the vegetable", "category": "food",     "cefr": "A2", "example": "Eet je groente, dat is gezond."},
    {"word": "het fruit",   "translation": "the fruit",     "category": "food",     "cefr": "A1", "example": "Ik eet elke dag fruit."},
    {"word": "het ei",      "translation": "the egg",       "category": "food",     "cefr": "A1", "example": "Twee eieren voor het ontbijt."},
    {"word": "de suiker",   "translation": "the sugar",     "category": "food",     "cefr": "A1", "example": "Doe je suiker in de koffie?"},
    {"word": "het zout",    "translation": "the salt",      "category": "food",     "cefr": "A1", "example": "Een beetje zout in de soep."},

    # ── Home & Objects ──────────────────────────────────────────────
    {"word": "het huis",    "translation": "the house",      "category": "home",    "cefr": "A1", "example": "Ons huis heeft drie kamers."},
    {"word": "de kamer",    "translation": "the room",       "category": "home",    "cefr": "A1", "example": "Mijn kamer is niet zo groot."},
    {"word": "de deur",     "translation": "the door",       "category": "home",    "cefr": "A1", "example": "Doe de deur dicht, het is koud."},
    {"word": "het raam",    "translation": "the window",     "category": "home",    "cefr": "A1", "example": "Het raam staat open."},
    {"word": "de tafel",    "translation": "the table",      "category": "home",    "cefr": "A1", "example": "De sleutels liggen op de tafel."},
    {"word": "de stoel",    "translation": "the chair",      "category": "home",    "cefr": "A1", "example": "Ga zitten op de stoel."},
    {"word": "het bed",     "translation": "the bed",        "category": "home",    "cefr": "A1", "example": "Ik ga om tien uur naar bed."},
    {"word": "de keuken",   "translation": "the kitchen",    "category": "home",    "cefr": "A1", "example": "We koken samen in de keuken."},
    {"word": "de badkamer", "translation": "the bathroom",   "category": "home",    "cefr": "A1", "example": "De badkamer is op de eerste verdieping."},
    {"word": "de sleutel",  "translation": "the key",        "category": "home",    "cefr": "A1", "example": "Ik ben mijn sleutel kwijt."},

    # ── Transport & Places ──────────────────────────────────────────
    {"word": "de auto",     "translation": "the car",        "category": "transport","cefr": "A1", "example": "De auto staat voor het huis."},
    {"word": "de fiets",    "translation": "the bicycle",    "category": "transport","cefr": "A1", "example": "In Nederland fietst iedereen."},
    {"word": "de trein",    "translation": "the train",      "category": "transport","cefr": "A1", "example": "De trein naar Utrecht vertrekt om drie uur."},
    {"word": "het station", "translation": "the station",    "category": "transport","cefr": "A2", "example": "We spreken af op het station."},
    {"word": "de straat",   "translation": "the street",     "category": "transport","cefr": "A1", "example": "Kinderen spelen op straat."},
    {"word": "de stad",     "translation": "the city",       "category": "transport","cefr": "A1", "example": "Amsterdam is een mooie stad."},
    {"word": "het dorp",    "translation": "the village",    "category": "transport","cefr": "A2", "example": "Zij woont in een klein dorp."},
    {"word": "de winkel",   "translation": "the shop",       "category": "transport","cefr": "A1", "example": "De winkel gaat om negen uur open."},
    {"word": "het vliegveld","translation": "the airport",   "category": "transport","cefr": "A2", "example": "Het vliegveld is ver van de stad."},

    # ── Time & Weather ──────────────────────────────────────────────
    {"word": "vandaag",     "translation": "today",          "category": "time",     "cefr": "A1", "example": "Vandaag is het maandag."},
    {"word": "morgen",      "translation": "tomorrow",       "category": "time",     "cefr": "A1", "example": "Morgen ga ik naar de dokter."},
    {"word": "gisteren",    "translation": "yesterday",      "category": "time",     "cefr": "A1", "example": "Gisteren was het lekker weer."},
    {"word": "nu",          "translation": "now",            "category": "time",     "cefr": "A1", "example": "Wat doe je nu?"},
    {"word": "later",       "translation": "later",          "category": "time",     "cefr": "A1", "example": "Ik bel je later terug."},
    {"word": "vroeg",       "translation": "early",          "category": "time",     "cefr": "A2", "example": "Ik sta vroeg op om te sporten."},
    {"word": "laat",        "translation": "late",           "category": "time",     "cefr": "A1", "example": "Het is laat, ik ga naar bed."},
    {"word": "de dag",      "translation": "the day",        "category": "time",     "cefr": "A1", "example": "Fijne dag nog!"},
    {"word": "de nacht",    "translation": "the night",      "category": "time",     "cefr": "A1", "example": "Het was een lange nacht."},
    {"word": "de week",     "translation": "the week",       "category": "time",     "cefr": "A1", "example": "Deze week heb ik vrij."},
    {"word": "het weer",    "translation": "the weather",    "category": "time",     "cefr": "A2", "example": "Het weer is slecht vandaag."},
    {"word": "de zon",      "translation": "the sun",        "category": "time",     "cefr": "A1", "example": "De zon schijnt vandaag."},
    {"word": "de regen",    "translation": "the rain",       "category": "time",     "cefr": "A1", "example": "De regen komt met bakken uit de lucht."},
    {"word": "koud",        "translation": "cold",           "category": "time",     "cefr": "A1", "example": "Het is koud buiten, draag een jas."},
    {"word": "warm",        "translation": "warm",           "category": "time",     "cefr": "A1", "example": "Het is warm vandaag, laten we gaan zwemmen."},

    # ── Common Adjectives ───────────────────────────────────────────
    {"word": "groot",       "translation": "big",            "category": "adjectives","cefr": "A1", "example": "Amsterdam is een grote stad."},
    {"word": "klein",       "translation": "small",          "category": "adjectives","cefr": "A1", "example": "Een klein kopje koffie graag."},
    {"word": "goed",        "translation": "good",           "category": "adjectives","cefr": "A1", "example": "Het eten is erg goed hier."},
    {"word": "slecht",      "translation": "bad",            "category": "adjectives","cefr": "A1", "example": "Het weer is slecht vandaag."},
    {"word": "mooi",        "translation": "beautiful",      "category": "adjectives","cefr": "A1", "example": "Wat een mooie jurk!"},
    {"word": "lelijk",      "translation": "ugly",           "category": "adjectives","cefr": "A2", "example": "Dat gebouw is echt lelijk."},
    {"word": "oud",         "translation": "old",            "category": "adjectives","cefr": "A1", "example": "Dit huis is heel oud."},
    {"word": "nieuw",       "translation": "new",            "category": "adjectives","cefr": "A1", "example": "Ik heb een nieuwe auto gekocht."},
    {"word": "lang",        "translation": "long / tall",    "category": "adjectives","cefr": "A1", "example": "Mijn broer is erg lang."},
    {"word": "kort",        "translation": "short",          "category": "adjectives","cefr": "A1", "example": "Het is een kort verhaal."},
    {"word": "snel",        "translation": "fast",           "category": "adjectives","cefr": "A1", "example": "De trein is heel snel."},
    {"word": "langzaam",    "translation": "slow",           "category": "adjectives","cefr": "A2", "example": "De bus is erg langzaam."},
    {"word": "duur",        "translation": "expensive",      "category": "adjectives","cefr": "A2", "example": "Deze wijn is te duur."},
    {"word": "goedkoop",    "translation": "cheap",          "category": "adjectives","cefr": "A2", "example": "De groente is goedkoop op de markt."},
    {"word": "makkelijk",   "translation": "easy",           "category": "adjectives","cefr": "A2", "example": "Nederlands is niet makkelijk!"},
    {"word": "moeilijk",    "translation": "difficult",      "category": "adjectives","cefr": "A2", "example": "Deze vraag is moeilijk."},
    {"word": "belangrijk",  "translation": "important",      "category": "adjectives","cefr": "A2", "example": "Dit is een belangrijke afspraak."},

    # ── Numbers ─────────────────────────────────────────────────────
    {"word": "een",         "translation": "one",            "category": "numbers",  "cefr": "A1", "example": "Ik heb een broer."},
    {"word": "twee",        "translation": "two",            "category": "numbers",  "cefr": "A1", "example": "Twee koffie, alsjeblieft."},
    {"word": "drie",        "translation": "three",          "category": "numbers",  "cefr": "A1", "example": "Drie keer per week sport ik."},
    {"word": "vier",        "translation": "four",           "category": "numbers",  "cefr": "A1", "example": "Het feest begint om vier uur."},
    {"word": "vijf",        "translation": "five",           "category": "numbers",  "cefr": "A1", "example": "Ik heb vijf minuten nodig."},
    {"word": "zes",         "translation": "six",            "category": "numbers",  "cefr": "A1", "example": "Zes eieren voor de cake."},
    {"word": "zeven",       "translation": "seven",          "category": "numbers",  "cefr": "A1", "example": "De winkel is open tot zeven uur."},
    {"word": "acht",        "translation": "eight",          "category": "numbers",  "cefr": "A1", "example": "Mijn zoon is acht jaar."},
    {"word": "negen",       "translation": "nine",           "category": "numbers",  "cefr": "A1", "example": "Het is negen uur 's ochtends."},
    {"word": "tien",        "translation": "ten",            "category": "numbers",  "cefr": "A1", "example": "Een tien voor je examen!"},
    {"word": "twintig",     "translation": "twenty",         "category": "numbers",  "cefr": "A1", "example": "Het kost twintig euro."},
    {"word": "honderd",     "translation": "hundred",        "category": "numbers",  "cefr": "A1", "example": "Honderd procent zeker!"},

    # ── Colors ──────────────────────────────────────────────────────
    {"word": "rood",        "translation": "red",            "category": "colors",   "cefr": "A1", "example": "De roos is rood."},
    {"word": "blauw",       "translation": "blue",           "category": "colors",   "cefr": "A1", "example": "De lucht is blauw."},
    {"word": "groen",       "translation": "green",          "category": "colors",   "cefr": "A1", "example": "Het gras is groen."},
    {"word": "geel",        "translation": "yellow",         "category": "colors",   "cefr": "A1", "example": "De zon is geel."},
    {"word": "zwart",       "translation": "black",          "category": "colors",   "cefr": "A1", "example": "De kat is zwart."},
    {"word": "wit",         "translation": "white",          "category": "colors",   "cefr": "A1", "example": "De muur is wit."},
    {"word": "oranje",      "translation": "orange",         "category": "colors",   "cefr": "A1", "example": "Oranje is de kleur van Nederland."},
    {"word": "paars",       "translation": "purple",         "category": "colors",   "cefr": "A2", "example": "Zij draagt een paarse jurk."},

    # ── Phrases / Survival ──────────────────────────────────────────
    {"word": "hoe gaat het?",           "translation": "how are you?",              "category": "phrases",  "cefr": "A1", "example": "Hoi, hoe gaat het met je?"},
    {"word": "ik begrijp het niet",      "translation": "I don't understand",        "category": "phrases",  "cefr": "A1", "example": "Sorry, ik begrijp het niet. Kun je dat herhalen?"},
    {"word": "ik spreek een beetje Nederlands","translation": "I speak a little Dutch","category": "phrases","cefr": "A1", "example": "Ik spreek een beetje Nederlands, maar niet vloeiend."},
    {"word": "spreekt u Engels?",       "translation": "do you speak English?",      "category": "phrases",  "cefr": "A1", "example": "Sorry, spreekt u Engels?"},
    {"word": "waar is het toilet?",     "translation": "where is the toilet?",       "category": "phrases",  "cefr": "A1", "example": "Pardon, waar is het toilet?"},
    {"word": "hoeveel kost dit?",       "translation": "how much does this cost?",   "category": "phrases",  "cefr": "A2", "example": "Hoeveel kost dit boek?"},
    {"word": "ik wil graag...",         "translation": "I would like...",            "category": "phrases",  "cefr": "A1", "example": "Ik wil graag een cappuccino."},
]

CATEGORIES = sorted(set(e["category"] for e in VOCABULARY))
BY_CATEGORY = {}
for entry in VOCABULARY:
    cat = entry["category"]
    BY_CATEGORY.setdefault(cat, []).append(entry)
