"""
Dutch survival phrases organized by real-world scenario.
Each entry: dutch, english, scenario, cefr.
"""

PHRASES = [
    # ── Restaurant / Café ─────────────────────────────────────────────
    {"dutch": "Mag ik de menukaart?",         "english": "Can I have the menu?",            "scenario": "restaurant", "cefr": "A1"},
    {"dutch": "Ik wil graag bestellen.",      "english": "I would like to order.",          "scenario": "restaurant", "cefr": "A1"},
    {"dutch": "Wat raadt u aan?",             "english": "What do you recommend?",          "scenario": "restaurant", "cefr": "A2"},
    {"dutch": "Ik heb een allergie voor...",  "english": "I am allergic to...",             "scenario": "restaurant", "cefr": "A2"},
    {"dutch": "De rekening, alstublieft.",    "english": "The bill, please.",               "scenario": "restaurant", "cefr": "A1"},
    {"dutch": "Heeft u een tafel voor twee?", "english": "Do you have a table for two?",    "scenario": "restaurant", "cefr": "A2"},
    {"dutch": "Eet smakelijk!",              "english": "Enjoy your meal!",                 "scenario": "restaurant", "cefr": "A1"},
    {"dutch": "Mag ik nog een glas water?",   "english": "Can I have another glass of water?","scenario": "restaurant","cefr": "A2"},
    {"dutch": "Was het lekker?",              "english": "Was it tasty?",                    "scenario": "restaurant", "cefr": "A2"},
    {"dutch": "Ik betaal contant.",           "english": "I'll pay in cash.",               "scenario": "restaurant", "cefr": "A2"},

    # ── Shopping ──────────────────────────────────────────────────────
    {"dutch": "Hoeveel kost dit?",            "english": "How much does this cost?",        "scenario": "shopping",  "cefr": "A1"},
    {"dutch": "Dat is te duur.",              "english": "That's too expensive.",            "scenario": "shopping",  "cefr": "A2"},
    {"dutch": "Heeft u dit in het blauw?",    "english": "Do you have this in blue?",        "scenario": "shopping",  "cefr": "A2"},
    {"dutch": "Mag ik het passen?",           "english": "Can I try it on?",                 "scenario": "shopping",  "cefr": "A2"},
    {"dutch": "Ik kijk alleen even.",         "english": "I'm just looking.",                "scenario": "shopping",  "cefr": "A1"},
    {"dutch": "Neemt u pinpas?",              "english": "Do you take debit card?",          "scenario": "shopping",  "cefr": "A2"},
    {"dutch": "Waar is de maat M?",           "english": "Where is the size M?",             "scenario": "shopping",  "cefr": "A2"},
    {"dutch": "Ik neem het mee.",             "english": "I'll take it.",                    "scenario": "shopping",  "cefr": "A1"},
    {"dutch": "Heeft u een tasje?",           "english": "Do you have a small bag?",         "scenario": "shopping",  "cefr": "A2"},
    {"dutch": "Tot hoe laat bent u open?",    "english": "Until what time are you open?",   "scenario": "shopping",  "cefr": "A2"},

    # ── Directions / Travel ───────────────────────────────────────────
    {"dutch": "Waar is het station?",         "english": "Where is the station?",           "scenario": "travel",    "cefr": "A1"},
    {"dutch": "Hoe kom ik bij het museum?",   "english": "How do I get to the museum?",      "scenario": "travel",    "cefr": "A2"},
    {"dutch": "Rechtdoor en dan links.",      "english": "Straight ahead and then left.",    "scenario": "travel",    "cefr": "A2"},
    {"dutch": "Is het ver lopen?",            "english": "Is it far to walk?",              "scenario": "travel",    "cefr": "A2"},
    {"dutch": "Ik ben de weg kwijt.",         "english": "I'm lost.",                        "scenario": "travel",    "cefr": "B1"},
    {"dutch": "Welke tram moet ik nemen?",    "english": "Which tram should I take?",        "scenario": "travel",    "cefr": "A2"},
    {"dutch": "Hoe laat vertrekt de trein?",  "english": "What time does the train leave?", "scenario": "travel",    "cefr": "A2"},
    {"dutch": "Een enkeltje Utrecht graag.",  "english": "A one-way ticket to Utrecht please.","scenario": "travel","cefr": "A2"},
    {"dutch": "Is dit de goede richting?",    "english": "Is this the right direction?",     "scenario": "travel",    "cefr": "A2"},
    {"dutch": "Waar kan ik een fiets huren?", "english": "Where can I rent a bike?",        "scenario": "travel",    "cefr": "A2"},

    # ── Small Talk ────────────────────────────────────────────────────
    {"dutch": "Hoe gaat het met je?",         "english": "How are you?",                    "scenario": "smalltalk", "cefr": "A1"},
    {"dutch": "Wat doe je voor werk?",        "english": "What do you do for work?",         "scenario": "smalltalk", "cefr": "A2"},
    {"dutch": "Waar kom je vandaan?",          "english": "Where are you from?",              "scenario": "smalltalk", "cefr": "A1"},
    {"dutch": "Ik woon in Amsterdam.",         "english": "I live in Amsterdam.",             "scenario": "smalltalk", "cefr": "A1"},
    {"dutch": "Leuk je te ontmoeten!",        "english": "Nice to meet you!",                "scenario": "smalltalk", "cefr": "A1"},
    {"dutch": "Wat zijn je hobby's?",         "english": "What are your hobbies?",           "scenario": "smalltalk", "cefr": "A2"},
    {"dutch": "Heb je een leuke dag gehad?",  "english": "Did you have a nice day?",         "scenario": "smalltalk", "cefr": "A2"},
    {"dutch": "Vind je het hier mooi?",       "english": "Do you find it beautiful here?",   "scenario": "smalltalk", "cefr": "A2"},
    {"dutch": "Tot morgen!",                 "english": "See you tomorrow!",                 "scenario": "smalltalk", "cefr": "A1"},
    {"dutch": "Veel succes!",                "english": "Good luck!",                        "scenario": "smalltalk", "cefr": "A2"},

    # ── Emergency / Help ──────────────────────────────────────────────
    {"dutch": "Kunt u mij helpen?",           "english": "Can you help me?",                 "scenario": "emergency", "cefr": "A1"},
    {"dutch": "Ik heb een dokter nodig.",     "english": "I need a doctor.",                 "scenario": "emergency", "cefr": "A2"},
    {"dutch": "Bel de politie!",              "english": "Call the police!",                 "scenario": "emergency", "cefr": "A2"},
    {"dutch": "Het is een noodgeval.",         "english": "It's an emergency.",               "scenario": "emergency", "cefr": "B1"},
    {"dutch": "Ik voel me niet lekker.",      "english": "I don't feel well.",               "scenario": "emergency", "cefr": "A2"},
    {"dutch": "Waar is het dichtstbijzijnde ziekenhuis?","english": "Where is the nearest hospital?","scenario": "emergency", "cefr": "B1"},
    {"dutch": "Ik ben mijn portemonnee kwijt.","english": "I lost my wallet.",              "scenario": "emergency", "cefr": "B1"},
    {"dutch": "Kunt u een ambulance bellen?", "english": "Can you call an ambulance?",       "scenario": "emergency", "cefr": "A2"},
    {"dutch": "Het spijt me.",               "english": "I'm sorry.",                        "scenario": "emergency", "cefr": "A1"},
    {"dutch": "Geen probleem.",               "english": "No problem.",                      "scenario": "emergency", "cefr": "A1"},
]

SCENARIOS = sorted(set(p["scenario"] for p in PHRASES))

BY_SCENARIO = {}
for phrase in PHRASES:
    s = phrase["scenario"]
    BY_SCENARIO.setdefault(s, []).append(phrase)
