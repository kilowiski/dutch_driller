"""
Dutch survival phrases organized by real-world scenario.
Each entry: dutch, english, scenario, cefr.
"""

PHRASES = [
    # ── Restaurant / Cafe ─────────────────────────────────────────────
    {"word": "Mag ik de menukaart?",         "translation": "Can I have the menu?",            "scenario": "restaurant", "cefr": "A1"},
    {"word": "Ik wil graag bestellen.",      "translation": "I would like to order.",          "scenario": "restaurant", "cefr": "A1"},
    {"word": "Wat raadt u aan?",             "translation": "What do you recommend?",          "scenario": "restaurant", "cefr": "A2"},
    {"word": "Ik heb een allergie voor...",  "translation": "I am allergic to...",             "scenario": "restaurant", "cefr": "A2"},
    {"word": "De rekening, alstublieft.",    "translation": "The bill, please.",               "scenario": "restaurant", "cefr": "A1"},
    {"word": "Heeft u een tafel voor twee?", "translation": "Do you have a table for two?",    "scenario": "restaurant", "cefr": "A2"},
    {"word": "Eet smakelijk!",              "translation": "Enjoy your meal!",                 "scenario": "restaurant", "cefr": "A1"},
    {"word": "Mag ik nog een glas water?",   "translation": "Can I have another glass of water?","scenario": "restaurant","cefr": "A2"},
    {"word": "Was het lekker?",              "translation": "Was it tasty?",                    "scenario": "restaurant", "cefr": "A2"},
    {"word": "Ik betaal contant.",           "translation": "I'll pay in cash.",               "scenario": "restaurant", "cefr": "A2"},

    # ── Shopping ──────────────────────────────────────────────────────
    {"word": "Hoeveel kost dit?",            "translation": "How much does this cost?",        "scenario": "shopping",  "cefr": "A1"},
    {"word": "Dat is te duur.",              "translation": "That's too expensive.",            "scenario": "shopping",  "cefr": "A2"},
    {"word": "Heeft u dit in het blauw?",    "translation": "Do you have this in blue?",        "scenario": "shopping",  "cefr": "A2"},
    {"word": "Mag ik het passen?",           "translation": "Can I try it on?",                 "scenario": "shopping",  "cefr": "A2"},
    {"word": "Ik kijk alleen even.",         "translation": "I'm just looking.",                "scenario": "shopping",  "cefr": "A1"},
    {"word": "Neemt u pinpas?",              "translation": "Do you take debit card?",          "scenario": "shopping",  "cefr": "A2"},
    {"word": "Waar is de maat M?",           "translation": "Where is the size M?",             "scenario": "shopping",  "cefr": "A2"},
    {"word": "Ik neem het mee.",             "translation": "I'll take it.",                    "scenario": "shopping",  "cefr": "A1"},
    {"word": "Heeft u een tasje?",           "translation": "Do you have a small bag?",         "scenario": "shopping",  "cefr": "A2"},
    {"word": "Tot hoe laat bent u open?",    "translation": "Until what time are you open?",   "scenario": "shopping",  "cefr": "A2"},

    # ── Directions / Travel ───────────────────────────────────────────
    {"word": "Waar is het station?",         "translation": "Where is the station?",           "scenario": "travel",    "cefr": "A1"},
    {"word": "Hoe kom ik bij het museum?",   "translation": "How do I get to the museum?",      "scenario": "travel",    "cefr": "A2"},
    {"word": "Rechtdoor en dan links.",      "translation": "Straight ahead and then left.",    "scenario": "travel",    "cefr": "A2"},
    {"word": "Is het ver lopen?",            "translation": "Is it far to walk?",              "scenario": "travel",    "cefr": "A2"},
    {"word": "Ik ben de weg kwijt.",         "translation": "I'm lost.",                        "scenario": "travel",    "cefr": "B1"},
    {"word": "Welke tram moet ik nemen?",    "translation": "Which tram should I take?",        "scenario": "travel",    "cefr": "A2"},
    {"word": "Hoe laat vertrekt de trein?",  "translation": "What time does the train leave?", "scenario": "travel",    "cefr": "A2"},
    {"word": "Een enkeltje Utrecht graag.",  "translation": "A one-way ticket to Utrecht please.","scenario": "travel","cefr": "A2"},
    {"word": "Is dit de goede richting?",    "translation": "Is this the right direction?",     "scenario": "travel",    "cefr": "A2"},
    {"word": "Waar kan ik een fiets huren?", "translation": "Where can I rent a bike?",        "scenario": "travel",    "cefr": "A2"},

    # ── Small Talk ────────────────────────────────────────────────────
    {"word": "Hoe gaat het met je?",         "translation": "How are you?",                    "scenario": "smalltalk", "cefr": "A1"},
    {"word": "Wat doe je voor werk?",        "translation": "What do you do for work?",         "scenario": "smalltalk", "cefr": "A2"},
    {"word": "Waar kom je vandaan?",          "translation": "Where are you from?",              "scenario": "smalltalk", "cefr": "A1"},
    {"word": "Ik woon in Amsterdam.",         "translation": "I live in Amsterdam.",             "scenario": "smalltalk", "cefr": "A1"},
    {"word": "Leuk je te ontmoeten!",        "translation": "Nice to meet you!",                "scenario": "smalltalk", "cefr": "A1"},
    {"word": "Wat zijn je hobby's?",         "translation": "What are your hobbies?",           "scenario": "smalltalk", "cefr": "A2"},
    {"word": "Heb je een leuke dag gehad?",  "translation": "Did you have a nice day?",         "scenario": "smalltalk", "cefr": "A2"},
    {"word": "Vind je het hier mooi?",       "translation": "Do you find it beautiful here?",   "scenario": "smalltalk", "cefr": "A2"},
    {"word": "Tot morgen!",                 "translation": "See you tomorrow!",                 "scenario": "smalltalk", "cefr": "A1"},
    {"word": "Veel succes!",                "translation": "Good luck!",                        "scenario": "smalltalk", "cefr": "A2"},

    # ── Emergency / Help ──────────────────────────────────────────────
    {"word": "Kunt u mij helpen?",           "translation": "Can you help me?",                 "scenario": "emergency", "cefr": "A1"},
    {"word": "Ik heb een dokter nodig.",     "translation": "I need a doctor.",                 "scenario": "emergency", "cefr": "A2"},
    {"word": "Bel de politie!",              "translation": "Call the police!",                 "scenario": "emergency", "cefr": "A2"},
    {"word": "Het is een noodgeval.",         "translation": "It's an emergency.",               "scenario": "emergency", "cefr": "B1"},
    {"word": "Ik voel me niet lekker.",      "translation": "I don't feel well.",               "scenario": "emergency", "cefr": "A2"},
    {"word": "Waar is het dichtstbijzijnde ziekenhuis?","translation": "Where is the nearest hospital?","scenario": "emergency", "cefr": "B1"},
    {"word": "Ik ben mijn portemonnee kwijt.","translation": "I lost my wallet.",              "scenario": "emergency", "cefr": "B1"},
    {"word": "Kunt u een ambulance bellen?", "translation": "Can you call an ambulance?",       "scenario": "emergency", "cefr": "A2"},
    {"word": "Het spijt me.",               "translation": "I'm sorry.",                        "scenario": "emergency", "cefr": "A1"},
    {"word": "Geen probleem.",               "translation": "No problem.",                      "scenario": "emergency", "cefr": "A1"},
]

SCENARIOS = sorted(set(p["scenario"] for p in PHRASES))
BY_SCENARIO = {}
for phrase in PHRASES:
    s = phrase["scenario"]
    BY_SCENARIO.setdefault(s, []).append(phrase)
